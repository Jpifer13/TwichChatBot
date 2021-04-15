"""
AuditorLog.py

This class creates the Auditor Log for a BFX 2.0 application.

Key changes

-----------
1/3/2020: SW Created.
 
"""
# Standard libraries
import os
import sys
from datetime import datetime, timedelta
import getpass     # Used to get the username. Works on Windows and Linux.
import platform    # Used to get the hostname. Works on Windows and Linux.

class AuditorLog:
    """
    Description
    -----------
    The Auditor Log is a human-readable format that provides the information an auditor wants to
    know about the run of an application.  The format of the log is as follows:

        Application: MyApplication
        Version:     Version 1.0
        Date/Time:   03Jan2020 17:38:13
        Hostname:    apple_py_auditor-log-latest-20200103-162947-879186625

    This log contains the following information:
        Application: the name of the application.
        Version: the version number of the application.
        Date/Time: the time that the application was run.
        User ID: the user ID of the person who ran the application.
        Hostname: the system on which the application was run. 
        Invocation: the invocation for the application, showing all command line arguments.
        Results: describes the result of the operation
        Inputs: a list of the inputs for this run. Each file that is read is listed.
        Outputs: a list of the outputs for this run. Each output file is listed.


    This log is distinct from an application log file, which contains the detailed information recorded
    during the running of the application. That log is used for troubleshooting. 
    """
    def __init__(self, applicationName: str, applicationVersion: str):
        """
        __init__ constructs a valid instance of the AuditorLog class. 

        Parameters
        ----------
            applicationName : String
                The name of the application (e.g. "IPA").
            applicationVersion : String
                The version number for this application (e.g. "Version 1.0.0").

        Raises
        ------
            ValueError 
                if the applicatiohName or applicationVersion are None or empty strings.            
        """
        # Values set by caller
        self._applicationName = applicationName
        self._version = applicationVersion
        if not applicationName:
            raise ValueError("You must specify the name of your application.")
        if not applicationVersion:
            raise ValueError(
                "You must specify the version number of your application.")
        # Values determined automatically
        self._username = getpass.getuser()
        self._hostname = platform.node()
        # Set the date/time to now
        self._startDateTime = datetime.now()
        self._officialDateTimeFormat = '%d%b%Y %H:%M:%S'
        self._filenameDateTimeFormat = '%Y_%m_%d_%H%M%S'
        # The filename for the log file
        self._filename = f"{self._applicationName}_{self._startDateTime.strftime(self._filenameDateTimeFormat)}.auditor.log"
        self._invocation = ' '.join(sys.argv)
        self._result = "Not specified"
        self._inputList = []
        self._outputList = []

    def setResult(self, result: str):
        """
        Sets the result of the application run, which is recorded in the log.

        Parameters
        ----------
            result : String
                The result from running this application: Success, Failure, etc.

        Raises
        ------
            ValueError 
                If the result is None or empty string.            
        """
        if result:
            self._result = result
        else:
            raise ValueError(
                "Result specified was either an empty string or None.")

    def addInput(self, inputString: str):
        """
        Adds an Input to the list of inputs for this application. In most cases, this is a fully qualified 
        path to an input file. Some applications may read information from a database or other non-file source. 

        Parameters
        ----------
            inputString : String
                A string with the fully qualified path to an input file or description of a non-file input. 

        Raises
        ------
            ValueError 
                if the inputString value is None or empty string.            
        """
        if inputString:
            self._inputList.append(inputString)
        else:
            raise ValueError(
                "Input specified was either an empty string or None.")

    def addOutput(self, outputString: str):
        """
        Adds an Output to the list of outputs for this application. In most cases, this should 
        be a fully qualified path for the output file. Call this function once for each output
        that is generated. Some applications may record that the output is written to a database 
        or other non-file location.

        Parameters
        ----------
            outputString : String
                A string with the fully qualified path to an output file or description of a non-file output. 

        Raises
        ------
            ValueError 
                if the outputString value is None or empty string.            
        """
        if outputString:
            self._outputList.append(outputString)
        else:
            raise ValueError(
                "Output specified was either an empty string or None.")

    def writeLogFile(self, directory=None):
        """
        Writes the Auditor Log to the specified directory. This function should be called at the end of 
        your program once you have listed all of the generated output files and recorded the result of 
        the application.

        If directory is None, writes the Auditor Log to the current working directory.
        Otherwise writes the Auditor Log to the specified directory.
        If the specified directory does not exist, a ValueError will be raised.

        The caller is responsible for handling any IOErrors that are raised. These will
        occur if the directory specified is not writable or if the current working directory
        is not writable (when no directory is specified). 

        Parameters
        ----------
            directory : String
                A fully qualitified path to the location to write the Auditor Log. The filename
                used is set by this class and cannot be altered by the caller. 

        Raises
        ------
            ValueError 
                if the specified directory does not exist.            
        """
        if directory:
            # Validate that the directory exists
            if not os.path.isdir(directory):
                raise ValueError(
                    f"Specified directory does not exist: {directory}.")
            # Prepend the location to the standard filename.
            self._filename = os.path.join(directory, self._filename)
        # This code does not handle IOError. If the specified location is not writable or the current
        # working directory is not writable (when no location is specified), the caller must handle
        # the exception.
        with open(self._filename, 'w') as file:
            file.write(
                "################################################################################\n")
            file.write(
                "# Q2 Solutions Auditor Log                                                     #\n")
            file.write(
                "################################################################################\n")
            file.write(f"Application: {self._applicationName}\n")
            file.write(f"Version:     {self._version}\n")
            file.write(
                f"Date/Time:   {self._startDateTime.strftime(self._officialDateTimeFormat)}\n")
            file.write(f"User ID:     {self._username}\n")
            file.write(f"Hostname:    {self._hostname}\n")
            file.write(f"Invocation:  {self._invocation}\n")
            file.write(f"Result:      {self._result}\n")
            # Write the list of inputs
            if not self._inputList:
                file.write("Inputs:      No Inputs\n")
            else:
                file.write("Inputs:\n")
                for anInput in self._inputList:
                    # Indented 13 columns to match the alignment of the above values
                    file.write(f"             {anInput}\n")
            # Write the list of outputs
            if not self._outputList:
                file.write("Outputs:     No Outputs\n")
            else:
                file.write("Outputs:\n")
                for anOutput in self._outputList:
                    # Indented 13 columns to match the alignment of the above values
                    file.write(f"             {anOutput}\n")
