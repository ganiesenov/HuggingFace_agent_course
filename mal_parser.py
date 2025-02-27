import requests
from bs4 import BeautifulSoup
import base64
from pathlib import Path

def test_parse_mal_image(url: str):
    """Test function for parsing anime image from MAL"""
    print(f"\nTesting image parse for URL: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print("Sending request...")
        response = requests.get(url, headers=headers)
        print(f"Response status code: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("\nTrying to find image with correct selector:")
        
        # Правильный селектор для основного изображения аниме
        img = soup.select_one('div.leftside img[data-src*="/images/anime/"]')
        if not img:
            img = soup.select_one('div.leftside img[src*="/images/anime/"]')
            
        if img:
            # Получаем URL изображения
            image_url = img.get('data-src') or img.get('src')
            if image_url:
                print(f"\nFound image URL: {image_url}")
                
                # Загружаем изображение
                print("Downloading image...")
                img_response = requests.get(image_url, headers=headers)
                if img_response.status_code == 200:
                    # Сохраняем локально
                    image_path = Path('anime_image.jpg')
                    image_path.write_bytes(img_response.content)
                    print(f"Image saved to {image_path.absolute()}")
                    
                    # Конвертируем в base64
                    image_base64 = base64.b64encode(img_response.content).decode('utf-8')
                    print(f"\nBase64 preview (first 100 chars): {image_base64[:100]}")
                    
                    return {
                        'success': True,
                        'image_url': image_url,
                        'local_path': str(image_path.absolute()),
                        'base64': image_base64
                    }
                else:
                    print(f"Failed to download image, status code: {img_response.status_code}")
                    return {'success': False, 'error': 'Failed to download image'}
            else:
                print("No image URL found in img tag")
                return {'success': False, 'error': 'No image URL found'}
        else:
            print("No image tag found")
            return {'success': False, 'error': 'No image tag found'}
            
    except Exception as e:
        print(f"Error parsing image: {str(e)}")
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    # Тестируем на странице FMA: Brotherhood
    test_url = "https://myanimelist.net/anime/5114/Fullmetal_Alchemist__Brotherhood"
    result = test_parse_mal_image(test_url)
    
    if result['success']:
        print("\nTest successful!")
        print(f"Image URL: {result['image_url']}")
        print(f"Saved to: {result['local_path']}")
    else:
        print(f"\nTest failed: {result.get('error')}")