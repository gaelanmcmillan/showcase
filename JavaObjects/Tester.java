/*
 * NAME:    Tester.java
 * AUTHOR:  Andrew meijer
 * DATE:    June 10, 2020     
 * RELATED FILES:            
 *          ObservableObject.java
 *          testingInstructions.txt (default name)
 *          expectedResults.txt     (default name)
 * PURPOSE: Read the instructions from testingInstructions.txt to create and remove objects,
 *          then observe and verify the results. Tests inherit from the Tester class.
 *          Tests are passed or failed by comapring an output file to expectedResults.txt
 * NOTES:   Commands to interact with the test space:
 *          CREATE  - creates a new observable object
 *          REMOVE  - removes an object with specified ID
 *          RESET   - empty the test space
 *          VIEW    - appends the current state to testResults.txt
 */

package JavaObjects;

import java.io.*;

public class Tester {
    //main
    public static void main(String[] args){
        //initialize the tester
        Tester firstTests = new Tester("testingInstructions.txt", "expectedResults.txt", "testResults.txt");
        System.out.println("Files verified.");

        //begin the test
        System.out.println("Beginning Tests.");
        
        //For each test... 
        for(){
            System.out.println();
        }
        //For each command...
            //validate the command
            //do the command
        //Use view command to output test results
        //Compare results with expected results to pass/fail the test
        //All Tests Passed
    }

    //variables
    ObservableObject[] currentObjects;
    String[] testingInstructionsFile;
    String[] expectedResultsContents;
    String[] testResultsContents;
    String testingInstructionsFilename;
    String expectedResultsFilename;
    String testResultsFilename;

    //constructors
    public Tester(){
        //offer to change from default name for testingInstructions.txt
        //offer to change from default name for expectedResults.txt
        //offer to change from default name for testResults.txt
    }
    public Tester(String instructions, String solution, String results){
        testingInstructionsFilename = instructions;
        expectedResultsFilename = solution;
        testResultsFilename = results;
        loadFileContents();
    }
    
    //methods
    //verify correct data files then input the data
    private void loadFileContents(){
        //variables
        int c1 = 0;
        int c2 = 0;
        FileInputStream testingInstructionsFile = null;
        FileInputStream expectedResultsFile = null;

        try{
             //establish a read connection with test instructions
            testingInstructionsFile = new FileInputStream(testingInstructionsFilename);

            //establish a read connection with expectedResults
            expectedResultsFile = new FileInputStream(expectedResultsFilename);

            //establish a read/write connection with testResults.txt
            testResultsFile = new FileOutputStream(testResultsFilename);

        } catch(FileNotFoundException e){
            System.out.println("File not found error.");
            System.exit(0);
        }
        System.out.println("Files connected.");

        /*read the first line of test instructions and expected results to confirm they are the same.
            -the first like should be an integer of the number of tests
            -Each test contains one command per line with an empty line between each test
        */
        try{
            c1 = testingInstructionsFile.read();
            c2 = expectedResultsFile.read();
        } catch(IOException e){
            System.out.println("File input error.");
            System.exit(0);
        }
        if(c1 != c2){
            System.out.println("Error: Number of tests doesn't match.");
        }

        //copy the file contents into the string arrays

    }//connectFiles

    //commands
    //output the test space to testResults
    public void view(){
        for(int i=0; i < currentObjects.length; i++){

        }
    }//view

    //create a new ObservableObject in the test space
    public void create(){

    }//create

    //remove a specified ObservableObject from the test space
    public void remove(){

    }//remove

    //remove all ObservableObjects from the test space
    public void reset(){

    }//reset

}//class