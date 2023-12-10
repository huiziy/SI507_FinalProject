

# 👟 Shoe Finder Application 👟

The Shoe Finder Application is a Python program that allows users to search for shoes based on various criteria such as shoe type, color, brand, price range, and rating. It fetches shopping results from an API, displays a selection interface, and provides the option to view product reviews.

### Getting Started
Follow these instructions to set up and run the Shoe Finder Application:

### Prerequisites

Python 3: Make sure you have Python 3 installed on your system. If not, you can download it from the official Python website.

### Installation
1. Clone this repository to your local machine:
```
git clone https://github.com/huiziy/SI507_FinalProject.git
```
2. Navigate to the project directory:
```  
cd SI507_FinalProject
```
3. Install the required Python packages using pip:
```
pip install -r requirements.txt
```
### API Key Setup

The Shoe Finder Application requires an API key to fetch shopping results. To use my API key (this API key is already hardcoded in the app.py):
```
api_key = "79cf37c845e6b957b3646abd88c9e138ebb038f2aae236a069260c442e27f0a8"
```
### Running the Application

You can run the Shoe Finder Application using the following command:
```
streamlit run shoefinder_app.py
```
This will start the application and open a web page in your default web browser.

### Interacting with the Application

- Shoe Selection: Choose the shoe type, color, brand, price range, and rating from the selection dropdowns on the left-hand side.
- Selection Results: The right-hand side will display the results based on your selections.
- Viewing Product Reviews: After selecting a product, click the "Fetch Reviews" button. You will see a link to the selected product's shop. The application will fetch and display product reviews, including keywords and top reviews.

### Troubleshooting
If you encounter any issues or errors, please make sure you have followed the installation and API key setup instructions correctly.
If you are still facing problems, feel free to contact the application developer for assistance.

### Contributing
Contributions to this project are welcome. If you find any bugs, have suggestions for improvements, or would like to add new features, please submit an issue or create a pull request.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
