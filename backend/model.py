"""
Model integration for vision-language model
Handles all AI model operations
"""
from typing import Any, TypeAlias
import torch
from PIL import Image
from pydantic import BaseModel, Field
from transformers import AutoModelForImageTextToText, AutoProcessor
from transformers.models.qwen2_vl.image_processing_qwen2_vl import smart_resize
import base64
from io import BytesIO

class ClickCoordinates(BaseModel):
    x: int = Field(ge=0, le=1000, description="The x coordinate, normalized between 0 and 1000.")
    y: int = Field(ge=0, le=1000, description="The y coordinate, normalized between 0 and 1000.")

ChatMessage: TypeAlias = dict[str, Any]

def initialize_model():
    """Initialize the model and processor"""
    model_name = "Hcompany/Holo2-4B"
    
    print(f"Loading model: {model_name}")
    print("This may take a few minutes on first run (downloading ~8GB)...")
    
    model = AutoModelForImageTextToText.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    processor = AutoProcessor.from_pretrained(model_name)
    
    return model, processor

def get_chat_messages(task: str, image: Image.Image) -> list[ChatMessage]:
    """Create the prompt structure for navigation task"""
    prompt = f"""Localize an element on the GUI image according to the provided target and output a click position.
     * You must output a valid JSON following the format: {ClickCoordinates.model_json_schema()}
     Your target is:"""
    
    return [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": f"{prompt}\n{task}"},
            ],
        },
    ]

def parse_reasoning(generated_ids: torch.tensor, processor) -> tuple[str, str]:
    """Parse content from generated_ids"""
    all_ids = generated_ids[0].tolist()
    
    try:
        think_start_index = all_ids.index(151667)
    except ValueError:
        think_start_index = -1
    
    try:
        think_end_index = all_ids.index(151668)
    except ValueError:
        think_end_index = len(all_ids)
    
    if think_start_index != -1:
        thinking_content = processor.decode(
            all_ids[think_start_index+1:think_end_index], 
            skip_special_tokens=True
        ).strip("\n")
        content = processor.decode(
            all_ids[think_end_index+1:], 
            skip_special_tokens=True
        ).strip("\n")
    else:
        thinking_content = ""
        content = processor.decode(generated_ids[0], skip_special_tokens=True).strip("\n")
    
    return content, thinking_content

def process_image_task(model, processor, image: Image.Image, task: str, task_type: str = "click"):
    """
    Process an image with a task using the vision model
    
    Args:
        model: The loaded vision model
        processor: The model processor
        image: PIL Image to process
        task: Task description (e.g., "Click on the button")
        task_type: Type of task (default: "click")
    
    Returns:
        dict: Processing results including coordinates and visualizations
    """
    try:
        # Pre-resize large images to reasonable size (SPEED OPTIMIZATION)
        MAX_DIMENSION = 1280  # Maximum width or height
        original_size = image.size
        if max(image.size) > MAX_DIMENSION:
            ratio = MAX_DIMENSION / max(image.size)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            print(f"Pre-resized image from {original_size} to {image.size} for faster processing")
        
        # Resize image according to model's image processor
        image_processor_config = processor.image_processor
        resized_height, resized_width = smart_resize(
            image.height,
            image.width,
            factor=image_processor_config.patch_size * image_processor_config.merge_size,
            min_pixels=image_processor_config.size.get("shortest_edge", None),
            max_pixels=image_processor_config.size.get("longest_edge", None),
        )
        processed_image = image.resize(
            size=(resized_width, resized_height), 
            resample=Image.Resampling.LANCZOS
        )
        
        # Create prompt
        messages = get_chat_messages(task, processed_image)
        
        # Apply chat template
        text_prompt = processor.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True, 
            thinking=False
        )
        
        inputs = processor(
            text=[text_prompt],
            images=[processed_image],
            padding=True,
            return_tensors="pt",
        ).to(model.device)
        
        # Generate response (optimized for speed)
        generated_ids = model.generate(
            **inputs, 
            max_new_tokens=32,
            do_sample=False,  # Faster than sampling
            pad_token_id=processor.tokenizer.pad_token_id
        )
        
        # Parse result
        content, thinking_content = parse_reasoning(generated_ids, processor)
        
        # Validate and parse result
        try:
            action = ClickCoordinates.model_validate_json(content)
            
            # Calculate actual pixel coordinates
            x_pixel = action.x / 1000 * processed_image.width
            y_pixel = action.y / 1000 * processed_image.height
            
            # Convert processed image to base64 for display
            buffered = BytesIO()
            processed_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                'task': task,
                'coordinates': {
                    'x': action.x,
                    'y': action.y,
                    'x_pixel': x_pixel,
                    'y_pixel': y_pixel
                },
                'processed_image': f'data:image/png;base64,{img_str}',
                'image_width': processed_image.width,
                'image_height': processed_image.height,
                'thinking': thinking_content,
                'raw_content': content
            }
        except Exception as e:
            return {
                'error': f'Failed to parse result: {str(e)}',
                'raw_content': content,
                'thinking': thinking_content
            }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            'error': f'Processing failed: {str(e)}'
        }

