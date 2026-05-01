from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
from BabyEagle3 import *
from PyQt6.QtCharts import *
import csv
import os

class USA(QMainWindow, Ui_StrongestSoldier):
    def __init__(self) -> None:
        """initializes the widget since this imports the baby eagle ui
        it then disables the back to menu button as long as hiding is
        until the vote button is pressed"""
        super().__init__()
        self.setupUi(self)
        self.BTMButton.setDisabled(True)
        self.BTMButton.hide()
        """This starts up the QSoundEffect tool and loads the sound and
        sets the volume and plays it when the application initializes"""
        self.SoundEffect = QSoundEffect()
        self.SoundEffect.setVolume(10)
        self.SoundEffect.setSource(QUrl.fromLocalFile("USA.wav"))
        self.SoundEffect.play()
        """This connects the the push buttons with their respective functions
        Votebutton basically being the submit function, the results button connecting
        display results function and then hiding and lowering the widget that contains
        the bar graphs and results from the user, so that the user can interact with the
        other buttons
        it also connects the Back to menu button that when pressed gets rid of the"""
        self.Votebutton.clicked.connect(self.Submit)
        self.ResultsButton.clicked.connect(self.DisplayResults)
        self.VoteWidget.hide()
        self.VoteWidget.lower()
        self.BTMButton.clicked.connect(self.ReturnToMenu)

    def votecheck(self) -> str:
        """This vote check function just goes and sees which radiobutton
        was selected when the submit button was pressed, if no candidate
        was selected it will simply return '' and ask the user to select a candidate"""
        if self.Agatha.isChecked():
            return 'Agatha'
        elif self.John.isChecked():
            return 'John'
        elif self.Jane.isChecked():
            return 'Jane'
        else:
            return ''

    def DisplayResults(self) -> None:
        """the display results function pulls counts, which is a dictionary
        of the candidates and the votes that the candidates have by scanning the csv file
        it then hides the other buttons like the vote button and the results button
        it also hides the text box and the line edit it also enables the Back to Menu button and
        shows itself so that the user can go back and vote if they wanted to.
        i also didnt figure this part out on my own, i had to go to the pyqt documentation document page
        to learn how to use the graphing and bar graphs functions"""
        counts = self.votecount()
        self.U.hide()
        self.Votebutton.hide()
        self.ResultsButton.hide()
        self.Text.hide()
        self.Agatha.hide()
        self.John.hide()
        self.Jane.hide()
        self.BTMButton.show()
        self.BTMButton.setDisabled(False)
        '''this part in the code is what i used to make my bar graphs
        pyqt6 has its own bargraph functions included so i first pull the names 
        and votes from the dictionary we got from a different function
        then we set up the graph, here we get all the information for the graphs stored'''
        candbars = QBarSet("Total Votes")
        candnames = list(counts.keys())
        candvotes = list(counts.values())
        candbars.append(candvotes)
        '''the information that is extracted is then put into a container which is the Qbarseries
        then i use the qchart function which is what is going to display the graph information
        we then add the information from the vote series which contains the numerical data
        from the candvotes and put it into the votechart'''
        voteseries = QBarSeries()
        voteseries.append(candbars)

        votechart = QChart()
        votechart.addSeries(voteseries)
        '''here i had to make custom x and y axis bars because the range
        of numbers on average is 0-6, so first i use two functions, one for the x axis
        and one for the y axis i then append the x axis the candidate names and for the y axis
        i just give a range of numbers that i want'''
        x_axis_names = QBarCategoryAxis()
        x_axis_names.append(candnames)
        y_axis_range = QValueAxis()
        y_axis_range.setRange(0, 100)
        '''here i connect the axis's with what graph i want them on and on what position i want 
        them to be displayed at'''
        votechart.addAxis(y_axis_range, Qt.AlignmentFlag.AlignLeft)
        voteseries.attachAxis(y_axis_range)
        votechart.addAxis(x_axis_names, Qt.AlignmentFlag.AlignBottom)
        voteseries.attachAxis(x_axis_names)

        '''here i set up the ability to actually display the chart
        i then add a chartlayout that is essentially just a QV box to display the info in
        then i add out votechart_view to be displayed inside of the chart layout
        then below since i added an extra widget box just for displaying the graph
        i then call the VoteWidget box and set it as the layout for the graphs show with
        the self.votewidget.setlayout(chartlayout) which connects the two together'''
        votechart_view = QChartView(votechart)

        chartlayout = QVBoxLayout()
        chartlayout.addWidget(votechart_view)
        '''finally i can show the widget box and pull it to the front so that it can be displayed'''
        self.VoteWidget.setLayout(chartlayout)
        self.VoteWidget.show()
        self.VoteWidget.raise_()
    def ReturnToMenu(self) -> None:
        """this return to menu function is tied to the back to menu push button
        when pressed, the function disables all of the display results buttons and widgets,
        this allows it to essentially go back to how the application was when initalized"""
        self.BTMButton.setDisabled(False)
        self.BTMButton.hide()
        self.VoteWidget.hide()
        self.VoteWidget.lower()
        self.Votebutton.show()
        self.ResultsButton.show()
        self.U.show()
        self.Text.show()
        self.John.show()
        self.Jane.show()
        self.Agatha.show()
        self.U.clear()
        self.text.clear()
        if self.buttonGroup.checkedButton() is not None:
            self.buttonGroup.setExclusive(False)
            self.buttonGroup.checkedButton().setChecked(False)
            self.buttonGroup.setExclusive(True)

    def votecount(self) -> dict[str, int]:
        """this vote count function sets up a library that stores the candidates and their votes
        it then goes through the Results.csv and goes through every line and checks for row[2] to who the
        candidate was, and if that candidate is in the votestallied library, it then adds 1 to the candidates total
        it then returns the votestallied which is called in the display results and used to build the bar graphs."""
        votestallied = {'Agatha':0, 'John':0, 'Jane':0}
        with open ('Results.csv', 'r', newline='') as infile:
            reader = csv.reader(infile, delimiter=',')
            for row in reader:
                candidate = row[1]
                if candidate in votestallied:
                    votestallied[candidate] += 1
        return votestallied

    def namecheck(self) -> str:
        """the namecheck function gets the users name from the U line edit
        it then strips it of whitespace and lowercases the name in case of case sensitive
        scenarios. it then goes through a first if statement which checks to make sure the name
        wasn't left blank and returns '', then if the name wasn't left blank, and if a results csv file
        hasnt even been made then it accepts the name as well. but if the results csv file is there, it
        then goes row by row and checks the first position and if that row[0] is the same as our users name
        then it returns '' and tells the user that they've already voted. If the csv file has been made but the
        name isn't in the csv file then it also returns the users name"""
        username = self.U.text().strip().lower()
        if username == '':
            self.Text.setText("Please enter a name")
            return ''
        if not os.path.isfile("Results.csv"):
            return username
        with open ('Results.csv', 'r', newline='') as readfile:
            reader = csv.reader(readfile, delimiter=',')
            for row in reader:
                if row[0] == username:
                    self.Text.setText("You have already voted")
                    return ''
        return username

    def Submit(self) -> None:
        """this pulls the users name and the candidate choice the user made when the vote button is clicked then
        and if statement checks to see if we got '' return from the name check function, the program doesnt proceed
        it then does the same to the candidate check, if we get a blank '' return from candidate then the program also stops
        from proceeding further, then i made a file_exists variable that checks if we have a results csv
        if it doesnt exist within our opening of the results.csv then it creates a new csv file called results.csv and makes
        and makes the header for it with the users name and the candidate. after everything is inputted, it then
        tells the user who they voted for and unselects the radio buttons, and clears the line edit
        """
        name = self.namecheck()
        if name == '':
            return
        candidate = self.votecheck()
        if candidate == '':
            return
        file_exists = os.path.isfile("Results.csv")
        with open ('Results.csv', 'a', newline='') as csvfile:
            content = csv.writer(csvfile, delimiter=',')
            if not file_exists:
                content.writerow(['name', 'candidate'])
            content.writerow([name, candidate])
        self.U.clear()
        self.Text.setText("Voted for " + candidate)
        if self.buttonGroup.checkedButton() is not None:
            self.buttonGroup.setExclusive(False)
            self.buttonGroup.checkedButton().setChecked(False)
            self.buttonGroup.setExclusive(True)

