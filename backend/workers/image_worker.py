import asyncio
import httpx
import logging
import os
from urllib.parse import quote
from workers.base_worker import BaseWorker
from utils.file_handler import FileHandler
from config import Config

logger = logging.getLogger(__name__)

class ImageWorker(BaseWorker):
    def __init__(self):
        super().__init__("generate_images", poll_interval=1.0)
        
    def process_task(self, input_data: dict, task_id: str) -> dict:
        """Generate images for script scenes using Pollinations.ai"""
        script = input_data.get('script')
        
        if not script or not script.get('scenes'):
            raise Exception('Script with scenes is required for image generation')
            
        logger.info(f"Generating images for {len(script['scenes'])} scenes")
        logger.info(f"Script title: '{script['title']}'")
        
        # Use asyncio to run async image generation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            images = loop.run_until_complete(self._generate_images_for_script(script))
        finally:
            loop.close()
        
        successful_images = [img for img in images if img.get('filepath') and not img.get('error')]
        failed_images = [img for img in images if img.get('error')]
        
        logger.info(f"Image generation completed:")
        logger.info(f"  Successful: {len(successful_images)}/{len(script['scenes'])}")
        if failed_images:
            logger.info(f"  Failed: {len(failed_images)}")
        
        return {
            'images': images,
            'script': script,
            'statistics': {
                'totalScenes': len(script['scenes']),
                'successfulImages': len(successful_images),
                'failedImages': len(failed_images),
                'successRate': round((len(successful_images) / len(script['scenes'])) * 100)
            },
            'message': f"Generated {len(successful_images)}/{len(script['scenes'])} images successfully"
        }
        
    async def _generate_images_for_script(self, script: dict) -> list:
        """Generate images for all scenes in the script"""
        images = []
        FileHandler.ensure_directories()
        
        for i, scene in enumerate(script['scenes']):
            filename = f"scene_{i + 1}.jpg"
            
            try:
                image_result = await self._generate_image(
                    scene['visualDescription'], 
                    filename
                )
                
                images.append({
                    'sceneIndex': i,
                    'filename': filename,
                    'filepath': image_result['filepath'],
                    'duration': scene['duration'],
                    'prompt': scene['visualDescription']
                })
                
                # Small delay between requests to be respectful
                await asyncio.sleep(1)
                
            except Exception as image_error:
                logger.error(f"Failed to generate image for scene {i + 1}: {image_error}")
                
                images.append({
                    'sceneIndex': i,
                    'filename': f"placeholder_{i + 1}.jpg",
                    'filepath': None,
                    'duration': scene['duration'],
                    'prompt': scene['visualDescription'],
                    'error': str(image_error)
                })
        
        logger.info(f"Generated {len([img for img in images if img.get('filepath')])}/{len(script['scenes'])} images")
        return images
        
    async def _generate_image(self, prompt: str, filename: str, width: int = 1024, height: int = 576) -> dict:
        """Generate a single image using Pollinations.ai"""
        try:
            # Clean and shorten the prompt
            clean_prompt = ''.join(c for c in prompt if c.isalnum() or c in ' -,.!?').strip()
            if len(clean_prompt) > 100:
                clean_prompt = clean_prompt[:100].strip()
                
            encoded_prompt = quote(clean_prompt)
            
            # Pollinations.ai API endpoint
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
            
            logger.info(f"Generating image: {clean_prompt[:50]}...")
            
            # Retry logic for network/API issues
            max_retries = 3
            
            for attempt in range(1, max_retries + 1):
                try:
                    logger.info(f"Attempt {attempt}/{max_retries}")
                    
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        response = await client.get(url, headers={
                            'User-Agent': 'VideoGenerator/1.0'
                        })
                        
                    if response.status_code == 200:
                        logger.info(f"Success on attempt {attempt}")
                        break
                    else:
                        raise Exception(f"HTTP {response.status_code}")
                        
                except Exception as retry_error:
                    logger.info(f"Attempt {attempt} failed: {retry_error}")
                    
                    if attempt == max_retries:
                        raise retry_error
                    
                    # Wait before retry (exponential backoff)
                    delay = attempt * 2
                    logger.info(f"Waiting {delay}s before retry...")
                    await asyncio.sleep(delay)
            
            # Save image to temp directory
            filepath = FileHandler.get_temp_path(filename)
            await FileHandler.save_binary(response.content, filepath)
            
            logger.info(f"Image saved: {filename}")
            return {
                'filepath': filepath,
                'prompt': clean_prompt,
                'filename': filename
            }
            
        except Exception as e:
            logger.error(f"Pollinations API error for '{prompt}': {e}")
            
            if 'timeout' in str(e).lower():
                raise Exception('Image generation timeout. Please try with a simpler prompt.')
            
            raise Exception(f"Pollinations API error: {e}")
            
    async def test_pollinations_connection(self):
        """Test Pollinations.ai connection"""
        try:
            result = await self._generate_image('A beautiful sunset over mountains', 'test_image.png', 512, 512)
            logger.info('Pollinations connection test successful')
            return result
        except Exception as e:
            logger.error(f'Pollinations connection test failed: {e}')
            raise