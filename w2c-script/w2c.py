# [import]
import csv
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Read in the data from the CSV file
with open('employee_data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    employee_data = list(reader)


# Loop through the employee data
for employee in employee_data[1:]:
    c = canvas.Canvas("c.pdf", pagesize=letter)
    c.setFont('Helvetica', 10)

    
    # Employee's address
    addressSplit = employee[40].strip().split(',')
    if len(addressSplit) > 3:
        c.drawString(319, 560, addressSplit[0] + "," + addressSplit[1]) #Box i Employee's address (street, apartment)
        c.drawString(319, 545, addressSplit[2] + "," + addressSplit[3]) #Box i Employee (town, zip, state)
    else:
        c.drawString(319, 560, addressSplit[0]) #Box i Employee's address (street)
        c.drawString(319, 545, addressSplit[1] + "," + addressSplit[2]) #Box i Employee's address (town, zip, state)
    
    
    # Draw employee data to the appropriate boxes on the W-2C form
    c.drawString(450, 690, employee[41]) #Employee's Social Security Number
            
    c.drawString(319, 581, employee[0]) #Employee's first name & middle initial
    c.drawString(456, 581, employee[1]) #Employee's last name

    c.drawString(45, 495, employee[10]) #Wages, tips, other compensation previous
    c.drawString(179, 495, employee[10]) #Wages, tips, other compensation corrected

    c.drawString(319, 495, employee[32]) #Fed income tax withheld previous
    c.drawString(456, 495, employee[32]) #Fed income tax withheld corrected

    c.drawString(45, 471, employee[12]) #Social Security wages previous
    c.drawString(179, 471, employee[12]) #Social Security wages corrected

    c.drawString(319, 471, employee[30]) #Social Security tax withheld previous
    c.drawString(456, 471, employee[30]) #Social Security tax withheld corrected

    c.drawString(45, 447, employee[11]) #Medicare wages and tips previous
    c.drawString(179, 447, employee[11]) #Medicare wages and tips correct

    c.drawString(319, 447, employee[28]) #Medicare tax withheld previous
    c.drawString(456, 447, employee[28]) #Medicare tax withheld correct

    
    if float(employee[7]) > 0:
        c.drawString(319, 399, str(employee[7])) #Dependent care benefits previous
        c.drawString(456, 399, str(employee[7])) #Dependent care benefits correct
    else:
        pass

    
    # Box 12 vars
    DDamount = float(employee[2]) + float(employee[3]) + float(employee[5]) + float(employee[42]) + float(employee[43]) + float(employee[44])
    roth401K = float(employee[4])
    simple401K = float(employee[6])
    
    
    # Checking box 12 codes
    if DDamount > 0 and roth401K > 0 and simple401K > 0:
        # Medical Spending
        c.drawString(319, 374, "DD") #Previous DD code
        c.drawString(350, 374, '{:.2f}'.format(DDamount)) #Previous medical spending

        c.drawString(456, 374, "DD") #Corrected DD code
        c.drawString(486, 374, '{:.2f}'.format(DDamount)) #Corrected DD spending

        # Roth 401k Spending
        c.drawString(319, 350, "AA") #Previous AA code
        c.drawString(350, 350, '{:.2f}'.format(roth401K)) #Previous Roth 401k Spending
        
        c.drawString(456, 350, "AA") #Corrected AA code
        c.drawString(486, 350, '{:.2f}'.format(roth401K)) #Corrected Roth 401k Spending

        # Simple 401k Spending
        c.drawString(319, 325, "D") #Previous D code
        c.drawString(350, 325, '{:.2f}'.format(simple401K)) # Previous 401k Spending

        c.drawString(456, 325, "D") #Corrected D code
        c.drawString(486, 325, '{:.2f}'.format(simple401K)) #Corrected 401k Spending
    
    elif DDamount > 0 and roth401K > 0 and simple401K == 0:
        # Medical Spending
        c.drawString(319, 374, "DD") #Previous DD code
        c.drawString(350, 374, '{:.2f}'.format(DDamount)) #Previous medical spending

        c.drawString(456, 374, "DD") #Corrected DD code
        c.drawString(486, 374, '{:.2f}'.format(DDamount)) #Corrected DD spending

        # Roth 401k Spending
        c.drawString(319, 350, "AA") #Previous AA code
        c.drawString(350, 350, '{:.2f}'.format(roth401K)) #Previous Roth 401k Spending
        
        c.drawString(456, 350, "AA") #Corrected AA code
        c.drawString(486, 350, '{:.2f}'.format(roth401K)) #Corrected Roth 401k Spending
    
    elif DDamount > 0 and roth401K == 0 and simple401K == 0:
        # Medical Spending
        c.drawString(319, 374, "DD") #Previous DD code
        c.drawString(350, 374, '{:.2f}'.format(DDamount)) #Previous medical spending

        c.drawString(456, 374, "DD") #Corrected DD code
        c.drawString(486, 374, '{:.2f}'.format(DDamount)) #Corrected DD spending
    
    elif DDamount == 0 and roth401K > 0 and simple401K == 0:
        # Roth 401k Spending
        c.drawString(319, 374, "AA") #Previous AA code
        c.drawString(350, 374, '{:.2f}'.format(roth401K)) #Previous Roth 401k spending

        c.drawString(456, 374, "AA") #Corrected AA code
        c.drawString(486, 374, '{:.2f}'.format(roth401K)) #Corrected Roth 401k spending

    elif DDamount == 0 and roth401K > 0 and simple401K > 0:
        # Roth 401k Spending
        c.drawString(319, 374, "AA") #Previous AA code
        c.drawString(350, 374, '{:.2f}'.format(roth401K)) #Previous Roth 401k spending

        c.drawString(456, 374, "AA") #Corrected AA code
        c.drawString(486, 374, '{:.2f}'.format(roth401K)) #Corrected Roth 401k spending

        # Simple 401k Spending
        c.drawString(319, 350, "D") #Previous D code
        c.drawString(350, 350, '{:.2f}'.format(simple401K)) #Previous 401k Spending
        
        c.drawString(456, 350, "D") #Corrected D code
        c.drawString(486, 350, '{:.2f}'.format(simple401K)) #Corrected 401k Spending

    elif DDamount == 0 and roth401K == 0 and simple401K > 0:
        # Simple 401k Spending
        c.drawString(319, 374, "D") #Previous D code
        c.drawString(350, 374, '{:.2f}'.format(simple401K)) #Previous medical spending

        c.drawString(456, 374, "D") #Corrected D code
        c.drawString(486, 374, '{:.2f}'.format(simple401K)) #Corrected D spending
    
    elif DDamount > 0 and roth401K == 0 and simple401K > 0:
        # Medical Spending
        c.drawString(319, 374, "DD") #Previous DD code
        c.drawString(350, 374, '{:.2f}'.format(DDamount)) #Previous medical spending

        c.drawString(456, 374, "DD") #Corrected DD code
        c.drawString(486, 374, '{:.2f}'.format(DDamount)) #Corrected DD spending
        
        # Simple 401k Spending
        c.drawString(319, 350, "D") #Previous D code
        c.drawString(350, 350, '{:.2f}'.format(simple401K)) #Previous Roth 401k Spending
        
        c.drawString(456, 350, "D") #Corrected D code
        c.drawString(486, 350, '{:.2f}'.format(simple401K)) #Corrected Roth 401k Spending
    
    else:
        pass

    
    # Checks if there is employee 401k or Roth 401k contributions
    if float(employee[4]) > 0 or float(employee[6]) > 0:

        # Draws a ✓ on retirement plan box
        c.drawString(87, 350, "✓")
        c.drawString(224, 350, "✓")
    
    else:
        pass
        
    
    #NY income tax Info
    c.drawString(45, 242, "NY") #State previous
    c.drawString(179, 242,"NY") #State corrected
    c.drawString(45, 220, "27-3545435") #Employer's NY state ID number
    c.drawString(179, 220, "27-3545435") #Employer's NY state ID number
    c.drawString(45, 195, employee[13]) #NY wages, tips, etc previous
    c.drawString(179, 195, employee[13]) #NY wages, tips, etc corrected
    c.drawString(45, 171, employee[26]) #State income tax NY previous
    c.drawString(179, 171, employee[26]) #State income tax NY corrected

    
    # Check if employee is from NJ, CT, PA, etc
    if 'NJ' in employee[40]:
        c.drawString(319, 242, "NJ") #Home state previous
        c.drawString(456, 242, "NJ") #Home state corrected
        c.drawString(319, 220, "273-545-435/000") #Employer's NJ state ID number previous
        c.drawString(456, 220, "273-545-435/000") #Employer's NJ state ID number corrected
        c.drawString(319, 195, employee[19]) #NJ wages, tips, etc previous
        c.drawString(456, 195, employee[19]) #NJ wages, tips, etc corrected
        c.drawString(319, 171, employee[27]) #NJ income tax previous
        c.drawString(456, 171, employee[27]) #NJ income tax corrected
        
        # Box 14 for NJ
        c.setFont('Helvetica', 7)
        c.drawString(45, 323, "NJ FLI: 0.00") #NJ FLI previous
        c.drawString(179, 317, "NJ FLI: 0.00") #NJ FLI corrected
        c.drawString(45, 317, "NJ SDI: " + employee[37]) #NJ SDI previous
        c.drawString(179, 311, "NJ SDI: " + employee[37]) #NJ SDI corrected
        c.drawString(45, 311, "NJ SUI: " + employee[36]) #NJ SUI previous
        c.drawString(179, 305, "NJ SUI: " + employee[36]) #NJ SUI corrected
        
        # Transit and parking spendature check
        if float(employee[9]) > 0 and float(employee[8]) == 0:
            c.drawString(45, 305, "Transit Pre-Tax: " + employee[9]) #Transit pre-tax previous
            c.drawString(179, 299, "Transit Pre-Tax: " + employee[9]) #Transit pre-tax corrected
        
        elif float(employee[9]) == 0 and float(employee[8]) > 0:
            c.drawString(45, 305, "Parking Pre-Tax: " + employee[8]) #Parking pre-tax previous
            c.drawString(179, 299, "Parking Pre-Tax: " + employee[8]) #Parking pre-tax corrected
        
        elif float(employee[9]) > 0 and float(employee[8]) > 0:
            c.drawString(45, 305, "Transit Pre-Tax: " + employee[9]) #Transit pre-tax previous
            c.drawString(179, 299, "Transit Pre-Tax: " + employee[9]) #Transit pre-tax corrected

            c.drawString(45, 299, "Parking Pre-Tax: " + employee[8]) #Parking pre-tax previous
            c.drawString(179, 293, "Parking Pre-Tax: " + employee[8]) #Parking pre-tax corrected
        
        else:
            pass
    
    elif 'PA' in employee[40]:
        c.drawString(319, 242, "PA") #Home state previous
        c.drawString(456, 242, "PA") #Home state corrected
        c.drawString(319, 220, "27-3545435") #Employer's PA state ID number previous
        c.drawString(456, 220, "27-3545435") #Employer's PA state ID number corrected
        c.drawString(319, 195, employee[15]) #PA wages, tips, etc previous
        c.drawString(456, 195, employee[15]) #PA wages, tips, etc corrected
        c.drawString(319, 171, employee[23]) #PA income tax previous
        c.drawString(456, 171, employee[23]) #PA income tax corrected

    elif 'VA' in employee[40]:
        c.drawString(319, 242, "VA") #Home state previous
        c.drawString(456, 242, "VA") #Home state corrected
        c.drawString(319, 220, "27-3545435") #Employer's VA state ID number previous
        c.drawString(456, 220, "27-3545435") #Employer's VA state ID number corrected
        c.drawString(319, 195, employee[16]) #VA wages, tips, etc previous
        c.drawString(456, 195, employee[16]) #VA wages, tips, etc corrected
        c.drawString(319, 171, employee[29]) #VA income tax previous
        c.drawString(456, 171, employee[29]) #VA income tax corrected

    elif 'CT' in employee[40]:
        c.drawString(319, 242, "CT") #Home state previous
        c.drawString(456, 242, "CT") #Home state corrected
        c.drawString(319, 220, "27-3545435") #Employer's CT state ID number previous
        c.drawString(456, 220, "27-3545435") #Employer's CT state ID number corrected
        c.drawString(319, 195, employee[17]) #CT wages, tips, etc previous
        c.drawString(456, 195, employee[17]) #CT wages, tips, etc corrected
        c.drawString(319, 171, employee[24]) #CT income tax previous
        c.drawString(456, 171, employee[24]) #CT income tax corrected

    elif 'MA' in employee[40]:
        c.drawString(319, 242, "MA") #Home state previous
        c.drawString(456, 242, "MA") #Home state corrected
        c.drawString(319, 220, "27-3545435") #Employer's MA state ID number previous
        c.drawString(456, 220, "27-3545435") #Employer's MA state ID number corrected
        c.drawString(319, 195, employee[18]) #MA wages, tips, etc previous
        c.drawString(456, 195, employee[18]) #MA wages, tips, etc corrected
        c.drawString(319, 171, employee[33]) #MA income tax previous
        c.drawString(456, 171, employee[33]) #MA income tax corrected

    elif 'MN' in employee[40]:
        c.drawString(319, 242, "MN") #Home state previous
        c.drawString(456, 242, "MN") #Home state corrected
        c.drawString(319, 220, "27-3545435") #Employer's MN state ID number previous
        c.drawString(456, 220, "27-3545435") #Employer's MN state ID number corrected
        c.drawString(319, 195, employee[20]) #MN wages, tips, etc previous
        c.drawString(456, 195, employee[20]) #MN wages, tips, etc corrected
        c.drawString(319, 171, employee[25]) #MN income tax previous
        c.drawString(456, 171, employee[25]) #MN income tax corrected

    elif 'OH' in employee[40]:
        c.drawString(319, 242, "OH") #Home state previous
        c.drawString(456, 242, "OH") #Home state corrected
        c.drawString(319, 220, "27-3545435") #Employer's OH state ID number previous
        c.drawString(456, 220, "27-3545435") #Employer's OH state ID number corrected
        c.drawString(319, 195, employee[21]) #OH wages, tips, etc previous
        c.drawString(456, 195, employee[21]) #OH wages, tips, etc corrected
        c.drawString(319, 171, employee[38]) #OH income tax previous
        c.drawString(456, 171, employee[38]) #OH income tax corrected

    elif 'CA' in employee[40]:
        c.drawString(319, 242, "CA") #Home state previous
        c.drawString(456, 242, "CA") #Home state corrected
        c.drawString(319, 220, "27-3545435") #Employer's CA state ID number previous
        c.drawString(456, 220, "27-3545435") #Employer's CA state ID number corrected
        c.drawString(319, 195, employee[22]) #CA wages, tips, etc previous
        c.drawString(456, 195, employee[22]) #CA wages, tips, etc corrected
        c.drawString(319, 171, employee[39]) #CA income tax previous
        c.drawString(456, 171, employee[39]) #CA income tax corrected

    else:
        pass


    # Checking and drawing NYC Locality information
    if float(employee[14]) + float(employee[34]) > 0:
        c.drawString(45, 122, employee[14]) #NY City wages, tips, etc previous
        c.drawString(179, 122, employee[14]) #NY City wages, tips, etc corrected
        c.drawString(45, 99, employee[34]) #NY City local income tax previous
        c.drawString(179, 99, employee[34]) #NY City local income tax corrected
        c.drawString(45, 75, "NYC") #Locality name previous
        c.drawString(179, 75, "NYC") #Locality name corrected
    
    else:
        pass


    # Box 14
    c.setFont('Helvetica', 7)
    c.drawString(45, 335, "NY SDI: " + employee[35]) #NY SDI withholding previous
    c.drawString(179, 329, "NY SDI: " + employee[35]) #NY SDI withholding corrected

    c.drawString(45, 329, "NY FLI: " + employee[31]) #NY FLI withholding previous
    c.drawString(179, 323, "NY FLI: " + employee[31]) #NY FLI withholding corrected


    c.drawString(179, 335, "SNY: " + employee[10]) #Box 14 corrected SNY
    

    # Transit
    if 'NJ' not in employee[40]:
        
        if float(employee[9]) > 0 and float(employee[8]) == 0:
            c.drawString(45, 323, "Transit Pre-Tax: " + employee[9])
            c.drawString(179, 317, "Transit Pre-Tax: " + employee[9])
        
        elif float(employee[9]) == 0 and float(employee[8]) > 0:
            c.drawString(45, 323, "Parking Pre-Tax: " + employee[8])
            c.drawString(179, 317, "Parking Pre-Tax: " + employee[8])
        
        elif float(employee[9]) > 0 and float(employee[8]) > 0:
            c.drawString(45, 323, "Transit Pre-Tax: " + employee[9])
            c.drawString(179, 317, "Transit Pre-Tax: " + employee[9])

            c.drawString(45, 317, "Parking Pre-Tax: " + employee[8])
            c.drawString(179, 311, "Parking Pre-Tax: " + employee[8])
        
        else:
            pass
    
    else:
        pass


    # Save the modified page
    c.save()


    # [init]
    output = PdfWriter()

    # take first file and open it 
    templatePDF = PdfReader(open("template.pdf", "rb"))

    # take the 2nd fiel and open it
    cPDF = PdfReader(open("c.pdf", "rb"))

    for i in range(6):
        templatePage = templatePDF.pages[i]

        # Merge both pages above
        templatePage.merge_page(cPDF.pages[0])

        # Add this created page to the output variable
        output.add_page(templatePage)

    # write+save the output to a pdf called `destination.pdf` 
    outputStream = open("w2c_form_"+ employee[0] + "_" + employee[1] + ".pdf", "wb")
    output.write(outputStream)

    outputStream.close()