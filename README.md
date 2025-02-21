# Flask Application for Google Drive File Processing with VertexAI

This Flask application is designed to run on Google Cloud Run and periodically checks specified Google Drive folders for new files using a service account. It processes new files by summarizing and formatting their content using Google's VertexAI, and then writes the summarized files back to a designated "Summaries Folder" on Google Drive.

## Features

- **Periodic API Calls**: The application periodically checks specified Google Drive folders for new files.
- **Transaction Management**: Uses an SQLite database to manage file processing states (pending, processed).
- **File Processing**: New files are processed using VertexAI for tasks such as summarizing and formatting Google Meet transcripts.
- **Automated File Handling**: Automatically writes processed files back to a specified "Summaries Folder" on Google Drive.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Google Cloud Account**: You need a Google Cloud account with billing enabled.
- **Service Account**: A Google Cloud service account with the necessary permissions to access Google Drive and VertexAI.
- **Google Cloud SDK**: Installed and configured on your local machine.
- **Python 3.8+**: The application is written in Python.

## Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file in the root directory and add the following variables:
   ```env
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-file.json
   DRIVE_FOLDER_ID=your-google-drive-folder-id
   SUMMARIES_FOLDER_ID=your-summaries-folder-id
   ```

4. **Initialize SQLite Database**
   Run the following command to initialize the SQLite database:
   ```bash
   python init_db.py
   ```

## Deployment to Google Cloud Run

1. **Build the Docker Image**
   ```bash
   docker build -t gcr.io/your-project-id/your-image-name .
   ```

2. **Push the Docker Image to Google Container Registry**
   ```bash
   docker push gcr.io/your-project-id/your-image-name
   ```

3. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy your-service-name --image gcr.io/your-project-id/your-image-name --platform managed
   ```

## Usage

Once deployed, the application will automatically:

1. Periodically check the specified Google Drive folders for new files.
2. Process new files using VertexAI.
3. Write summarized files back to the "Summaries Folder" on Google Drive.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Cloud Platform
- Flask
- VertexAI

---

For any questions or issues, please open an issue on the GitHub repository.