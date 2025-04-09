import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import os


def connect_to_email(email_address, password, imap_server="imap.gmail.com"):
    """Connect to email server and return IMAP connection"""
    try:
        # Create connection
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(email_address, password)
        return imap
    except Exception as e:
        print(f"Error connecting to email: {e}")
        return None

def get_latest_newsletter(imap, sender_address, save_path="newsletters"):
    """Fetch the latest newsletter from specified sender and save as text"""
    try:
        # Select inbox
        imap.select("INBOX")
        
        # Search for emails from newsletter sender
        _, messages = imap.search(None, f'FROM "{sender_address}"')
        
        if not messages[0]:
            print("No newsletters found")
            return
        
        # Get the latest email (last in the list)
        latest_email_id = messages[0].split()[-1]
        
        # Fetch email data
        _, data = imap.fetch(latest_email_id, "(RFC822)")
        email_body = data[0][1]
        
        # Parse email
        message = email.message_from_bytes(email_body)
        
        # Get subject
        subject, encoding = decode_header(message["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")
            
        # Get date
        date_str = message["Date"]
        date_obj = email.utils.parsedate_to_datetime(date_str)
        formatted_date = date_obj.strftime("%Y%m%d")
        
        # Extract text content
        text_content = ""
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    text_content = part.get_payload(decode=True).decode()
                    break
                elif part.get_content_type() == "text/html":
                    html_content = part.get_payload(decode=True).decode()
                    # Convert HTML to text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    text_content = soup.get_text(separator='\n', strip=True)
                    break
        else:
            content = message.get_payload(decode=True).decode()
            if message.get_content_type() == "text/html":
                soup = BeautifulSoup(content, 'html.parser')
                text_content = soup.get_text(separator='\n', strip=True)
            else:
                text_content = content
        
        # Create save directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        
        # Save to file
        filename = f"{save_path}/{formatted_date}_{subject.replace(' ', '_')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text_content)
            
        print(f"Newsletter saved to: {filename}")
        
    except Exception as e:
        print(f"Error processing email: {e}")
    finally:
        imap.close()
        imap.logout()

if __name__ == "__main__":
    # Configure these variables
    EMAIL_ADDRESS = "your_email@example.com"
    EMAIL_PASSWORD = "your_password"  # For Gmail, use App Password
    NEWSLETTER_SENDER = "newsletter@example.com"
    
    # Connect to email
    imap = connect_to_email(EMAIL_ADDRESS, EMAIL_PASSWORD)
    if imap:
        get_latest_newsletter(imap, NEWSLETTER_SENDER)
