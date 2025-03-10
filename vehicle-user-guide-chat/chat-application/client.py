import requests
import sys
import sys

def main():
    if len(sys.argv) < 2:
        print("Not enough arguments provided. Please invoke with servername and port as param 1 and param 2 respectively.")
        return
    args = sys.argv[1:]
    server = args[0]
    server = server or 'localhost'
    port = args[1]
    url = 'http://'+server+':'+str(port)+'/llm'
    print("Welcome to the car user guide GEN AI chat application. Please type a question about car features, or type exit to quit the application.")
    while True:
        try:
            question = input("\nYou: ")
            if len(question) > 0:
                if question.lower() == "exit":
                    break
                response = requests.post(url, data={'input': str(question)}, stream=True, timeout=(5,60))
                response.raise_for_status()
            
                # Process the streaming response
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    # Print without newline and flush immediately
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                
        except requests.exceptions.RequestException as e:
            print(f"\nAn error occurred: {e}")

if __name__ == '__main__':
    main()
