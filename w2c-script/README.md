# The Story Behind the Script
Our team received a notification that more than 100 of our coworker's W2s contained errors due to a payroll system malfunction. The finance department attempted to find prebuilt software solutions to correct these issues, but failed. We  promptly recognized the urgency of correcting the mistakes and issuing new, accurate W2s.

To accomplish this, I wrote a Python script that would read employee data from the corrected CSV file and generate W2-Cs as PDF files. 
The script uses the PyPDF2 library to manipulate PDFs and the ReportLab library to generate new PDFs with corrected data.

# What the Script Does
The script reads employee data from a CSV file named employee_data.csv using the csv library. The first row of the CSV file is ignored as it contains the column headers. 
The remaining rows of the file contain the employee data that is read into a list named employee_data.

The script then loops through each employee in the employee_data list, retrieves the required values from the list, and uses the reportlab library to generate a new PDF with corrected values.

The reportlab library provides a Canvas object that is used to create a new PDF. The setFont() method is used to set the font for the text that will be drawn on the PDF. 
The employee's address is split and drawn in onto the PDF. The Social Security Number and employee's name are also drawn on the PDF.

The corrected values for wages, tips, other compensation, federal income tax withheld, Social Security wages, Social Security tax withheld, Medicare wages and tips, and Medicare tax withheld are all drawn on the PDF. 
If an employee has dependent care benefits, they are also drawn on the PDF.

Finally, the script checks if an employee has values for medical spending, Roth 401k spending, and 401k spending. If an employee has values for all three, they are drawn on the PDF in the appropriate boxes. 
If an employee has values for medical spending and Roth 401k spending only, or any other combination of the three, those values are drawn on the PDF.

# How to Execute the Script
1. Have employee_data.csv, w2c.py, and template.pdf all in one folder on your desktop titled "W2C Project"

2. Open CMD by searching for it in the search bar

3. Write "cd Desktop" and press enter

4. Write "cd W2C Project" and press enter

5. Write pip install csv and press enter

6. Write pip install PyPDF2 and press enter

7. Write pip install reportlab and press enter

8. Write py w2c.py and press enter
