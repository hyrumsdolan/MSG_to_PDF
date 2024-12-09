import extract_msg
import os
import shutil

location = './msg_input/'
result_location = './pdf_output/'

# Clear the output folder before processing
if os.path.exists(result_location):
    for filename in os.listdir(result_location):
        file_path = os.path.join(result_location, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
else:
    os.makedirs(result_location)

# Process each .msg file in the location folder
files = os.listdir(location)
for file in files:
    if file not in [".DS_Store"]:
        print(file)
        filepath = os.path.join(location, file)
        
        # Open and extract message as a PDF
        with extract_msg.openMsg(filepath) as msg:
            response = msg.save(pdf=True)
            print(response)
        
        # Get the file path from response
        file_path = response[1]
        print(file_path)
        
        # Extract the filename (last part) from response
        new_filename = os.path.basename(file_path).split(' ',1)[1] + '.pdf'
        
        # Define the source and destination paths
        source_pdf = os.path.join(file_path, 'message.pdf')  
        destination_pdf = os.path.join(result_location, new_filename)
        
        # Move and rename the PDF file
        if os.path.exists(source_pdf):
            shutil.move(source_pdf, destination_pdf)
            print(f"Moved and renamed {source_pdf} to {destination_pdf}")
            
            # Remove the folder after moving the PDF
            shutil.rmtree(file_path)
            print(f"Deleted folder {file_path}")
        else:
            print(f"No message.pdf found in {file_path}")
