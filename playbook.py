def ask_question(question):
    """This function asks a question and returns a Yes or No response."""
    while True:
        response = input(question + " (Yes/No): ").strip().lower()
        if response in ['yes', 'no']:
            return response
        print("Invalid input! Please enter 'Yes' or 'No'.")

def troubleshoot():
    """This function represents the flow of troubleshooting steps."""
    
    # Step 1
    response = ask_question("Is the controller in Automatic Local mode with the proper setpoint?")
    if response == 'no':
        print("Action: Place the controller in Automatic mode with the proper setpoint.")
        return
    
    # Step 2
    response = ask_question("If the control loop is cascaded, is the primary controller in Auto mode?")
    if response == 'no':
        print("Action: Place the primary controller in Auto mode.")
        return

    # Step 3
    response = ask_question("If the control loop is cascaded, is the final controller in Cascade mode?")
    if response == 'no':
        print("Action: Place the final controller in Cascade mode.")
        return

    # Step 4
    response = ask_question("Is there an oscillating variation between the process variable and the setpoint?")
    if response == 'yes':
        response = ask_question("Does the control valve respond to controller output changes?")
        if response == 'no':
            print("Action: Have an instrumentation technician inspect and calibrate/repair the control valve.")
            return
        
    # Step 5
    response = ask_question("Is the control valve operating within a controlling range of 20-80%?")
    if response == 'no':
        print("Action: Consult with supervisor and consider either operating the control valve in Manual mode or partially bypassing the control valve.")
        return

    # Step 6
    response = ask_question("Does the process variable match the setpoint?")
    if response == 'no':
        print("Action: Have an instrumentation technician inspect and calibrate/repair the control valve.")
        return

    # Step 7
    response = ask_question("Does the field check of the control valve’s physical position closely match the flow controller’s output?")
    if response == 'no':
        print("Action: Bypass the transmitter and blowdown the transmitter sensing element, or have an instrumentation technician inspect and calibrate/repair the instrument.")
        return

    # If all checks passed
    print("Troubleshooting completed: No further action required. Consult the supervisor for any additional recommendations.")

if __name__ == "__main__":
    troubleshoot()
