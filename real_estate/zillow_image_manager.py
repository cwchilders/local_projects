from bs4 import BeautifulSoup

def extract_image_src(html_content):
    """
    Extracts the image source URL from the provided HTML snippet.
    
    Args:
        html_content (str): A string containing the HTML to parse.
        
    Returns:
        str: The URL of the image, or None if not found.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the <li> tag with the specific class
    list_item = soup.find('li', class_='media-stream-tile')
    
    if list_item:
        # Inside the <li>, find the <img> tag
        img_tag = list_item.find('img')
        
        if img_tag:
            # Get the value of the 'src' attribute
            return img_tag.get('src')
            
    return None


# --- Example Usage ---
if __name__ == "__main__":
    html_snippet = """<li class="Tile__StyledTile-fshdp-8-111-1__sc-gw6377-0 kttjLL media-stream-tile media-stream-tile--prominent" role="listitem"><figure><button aria-label="view larger view of the 1 photo of this home" class="sc-hLBbgP StyledCommonComponents__StyledBareButton-fshdp-8-111-1__sc-12pcmv4-6 hnVXxg bxzEYp"><picture class="sc-jNJNQp ftGxJm"><source type="image/webp" srcset="https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_192.webp 192w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_384.webp 384w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_576.webp 576w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_768.webp 768w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_960.webp 960w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_1152.webp 1152w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_1344.webp 1344w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_1536.webp 1536w" sizes="(min-width: 1280px) 768px, (min-width: 1024px) 60vw, (min-width: 900px) 60vw, (min-width: 768px) 55vw, 100vw"><source type="image/jpeg" srcset="https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_192.jpg 192w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_384.jpg 384w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_576.jpg 576w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_768.jpg 768w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_960.jpg 960w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_1152.jpg 1152w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_1344.jpg 1344w, https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_1536.jpg 1536w" sizes="(min-width: 1280px) 768px, (min-width: 1024px) 60vw, (min-width: 900px) 60vw, (min-width: 768px) 55vw, 100vw"><img src="https://photos.zillowstatic.com/fp/fb0e88d02d8b25a69f7f5c0520a4724f-cc_ft_960.jpg" alt=""></picture></button></figure></li>"""
    
    extracted_src = extract_image_src(html_snippet)
    if extracted_src:
        print(f"Extracted image source: {extracted_src}")
    else:
        print("Image source not found.")
