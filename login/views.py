# views.py
from django.shortcuts import render, redirect
import csv
import datetime
from django.shortcuts import render
def signup_view(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        gender = request.POST.get('gender')


        # Check if user already exists in CSV file
        with open('signup_data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[2] == email:
                    return render(request, 'signup.html', {'error_message': 'User with this email already exists.'})

        # Check if passwords match
        if password != repeat_password:
            return render(request, 'signup.html', {'error_message': 'Passwords do not match.'})

        # Save data to CSV file
        with open('signup_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([first_name, last_name, email, password, gender])

        # Redirect to login page after successful signup
        return redirect('login')  # Assuming you have a URL named 'login'
    else:
        return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Perform authentication (you may use Django's built-in authentication)
        # For simplicity, I'm assuming authentication is successful
        # Check if login credentials match signup data
        with open('signup_data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[2] == username:
                    if row[3] == password:
                        # Save login data to CSV
                        with open('login_data.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([username, password])
                        # Set email in session
                        request.session['email'] = username
                        return redirect('dashboard')  # Redirect to dashboard after successful login
                    else:
                        return render(request, 'login.html', {'error_message': 'Password is wrong.'})
        # If user not found in signup data
        return render(request, 'login.html', {'error_message': 'User does not exist.'})
    else:
        return render(request, 'login.html')


import csv
from django.shortcuts import render

def dashboard_view(request):
    # Load user information from the CSV file
    with open('signup_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        user_info = None
        for row in reader:
            print("Row:", row)  # Print the entire row
            if len(row) < 5:
                print("Incomplete row:", row)
            else:
                if row[2] == request.session.get('email'):
                    print("User found in CSV file:", row)
                    user_info = {
                        'first_name': row[0],
                        'last_name': row[1],
                        'email': row[2],
                        'gender': row[4],
                        # Add more user information as needed
                    }
                    break

    # Check if user info is found
    if user_info:
        print("User info:", user_info)
        return render(request, 'dashboard.html', {'user_info': user_info})
    else:
        # Handle case where user info is not found (e.g., user not logged in)
        return render(request, 'dashboard.html', {'error_message': 'User information not found.'})

