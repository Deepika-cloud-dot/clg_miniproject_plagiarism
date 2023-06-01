#!/usr/bin/env python
# coding: utf-8

import numpy as np
import glob
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1

    matrix = np.zeros((size_x, size_y))

    for x in range(size_x):
        matrix[x, 0] = x  # row aray with elements of x
    for y in range(size_y):
        matrix[0, y] = y  # column array with elements of y
    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:  # if the alphabets at the postion is same
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )

            else:         # if the alphabbets at the position are different
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1] + 1,
                    matrix[x, y-1] + 1
                )

    # returning the levenshtein distance
    return (matrix[size_x - 1, size_y - 1])


# OPTION 01: COMPARE ALL FILES IN FOLDER WITH MASTERFILE
def compare_folder_with_masterfile():

    def perform_folder_comparison():
        # Get the percentage of plagiarism allowed
        plag = int(percentage_entry.get())

        # Get the folder path
        folder_path = folder_path_var.get()

        # Get the masterfile path
        masterfile_path = masterfile_path_var.get()

        # Read the contents of the masterfile
        with open(masterfile_path, 'r') as masterfile:
            masterfile_data = masterfile.read().replace('\n', '')
            masterfile_str = masterfile_data.replace(' ', '')

        # Initialize a list to store plagiarized files
        plagiarized_files = []

        # Iterate over each text file in the folder
        for file_name in glob.glob(os.path.join(folder_path, '*.txt')):
            # Read the contents of the file
            with open(file_name, 'r') as file:
                file_data = file.read().replace('\n', '')
                file_str = file_data.replace(' ', '')

            # Determine the length for normalization
            if len(masterfile_str) > len(file_str):
                length = len(masterfile_str)
            else:
                length = len(file_str)

            # Calculate the similarity percentage
            similarity = 100 - \
                round((levenshtein(masterfile_str, file_str) / length) * 100, 2)

            # Check if the similarity percentage exceeds the plagiarism threshold
            if similarity > plag:
                plagiarized_files.append(file_name)

        # Display the plagiarized files in a message box
        if len(plagiarized_files) > 0:
            message = "Plagiarized files are:\n\n" + \
                "\n".join(plagiarized_files)
        else:
            message = "No plagiarized files"

        messagebox.showinfo("Plagiarism Checker", message)

    # Create a new window for the plagiarism comparison
    comparison_window = tk.Toplevel(window)
    comparison_window.title("Compare Folder with Masterfile")

    # Create and place the GUI elements
    label_percentage = tk.Label(
        comparison_window, text="Enter the percentage of plagiarism allowed:")
    label_percentage.pack()

    percentage_entry = tk.Entry(comparison_window)
    percentage_entry.pack()

    # Variables to store the folder and masterfile paths
    folder_path_var = tk.StringVar()
    masterfile_path_var = tk.StringVar()

    button_browse_folder = tk.Button(
        comparison_window, text="Browse Folder", command=lambda: browse_folder_path(folder_path_var))
    button_browse_folder.pack()

    button_browse_masterfile = tk.Button(
        comparison_window, text="Browse Masterfile", command=lambda: browse_masterfile_path(masterfile_path_var))
    button_browse_masterfile.pack()

    button_compare = tk.Button(
        comparison_window, text="Compare", command=perform_folder_comparison)
    button_compare.pack()

    comparison_window.mainloop()


# OPTION 02: COMPARE TWO FILES
def compare_two_files():
    def perform_comparison():
        # Get the percentage of plagiarism allowed
        plag = int(percentage_entry.get())

        # Get the paths of the two files
        file1_path = file1_path_var.get()
        file2_path = file2_path_var.get()

        # Read the contents of the first file
        with open(file1_path, 'r') as file1:
            file1_data = file1.read().replace('\n', '')
            file1_str = file1_data.replace(' ', '')

        # Read the contents of the second file
        with open(file2_path, 'r') as file2:
            file2_data = file2.read().replace('\n', '')
            file2_str = file2_data.replace(' ', '')

        # Determine the length for normalization
        if len(file1_str) > len(file2_str):
            length = len(file1_str)
        else:
            length = len(file2_str)

        # Calculate the similarity percentage
        similarity = 100 - \
            round((levenshtein(file1_str, file2_str) / length) * 100, 2)

        # Display the similarity percentage in a message box
        message = f"The similarity between the two files is {similarity}%."
        if similarity > plag:
            message += " Plagiarism detected!"
        else:
            message += " No plagiarism detected."

        messagebox.showinfo("Plagiarism Checker", message)

    # Create a new window for the file comparison
    comparison_window = tk.Toplevel(window)
    comparison_window.title("Compare Two Files")

    # Create and place the GUI elements
    label_percentage = tk.Label(
        comparison_window, text="Enter the percentage of plagiarism allowed:")
    label_percentage.pack()

    percentage_entry = tk.Entry(comparison_window)
    percentage_entry.pack()

    # Variables to store the paths of the two files
    file1_path_var = tk.StringVar()
    file2_path_var = tk.StringVar()

    button_browse_file1 = tk.Button(
        comparison_window, text="Browse File 1", command=lambda: browse_file1_path(file1_path_var))
    button_browse_file1.pack()

    button_browse_file2 = tk.Button(
        comparison_window, text="Browse File 2", command=lambda: browse_file2_path(file2_path_var))
    button_browse_file2.pack()

    button_compare = tk.Button(
        comparison_window, text="Compare", command=perform_comparison)
    button_compare.pack()

    comparison_window.mainloop()


# OPTION 03: COMPARE ALL FILES IN A FOLDER
def compare_all_files_in_folder():
    # Function to compare all files in a folder for plagiarism

    def perform_comparison():
        # Get the percentage of plagiarism allowed
        plag = int(percentage_entry.get())

        # Get the folder path
        folder_path = folder_path_var.get()

        # Read all the text files in the folder and store them in a list
        file_list = glob.glob(os.path.join(folder_path, '*.txt'))

        # Initialize a list to store plagiarized files
        plagiarized_files = []

        # Iterate over each pair of files for comparison
        for i in range(len(file_list)):
            for j in range(i + 1, len(file_list)):
                file1_path = file_list[i]
                file2_path = file_list[j]

                # Read the contents of the first file
                with open(file1_path, 'r') as file1:
                    file1_data = file1.read().replace('\n', '')
                    file1_str = file1_data.replace(' ', '')

                # Read the contents of the second file
                with open(file2_path, 'r') as file2:
                    file2_data = file2.read().replace('\n', '')
                    file2_str = file2_data.replace(' ', '')

                # Determine the length for normalization
                if len(file1_str) > len(file2_str):
                    length = len(file1_str)
                else:
                    length = len(file2_str)

                # Calculate the similarity percentage
                similarity = 100 - \
                    round((levenshtein(file1_str, file2_str) / length) * 100, 2)

                # Check if the similarity percentage exceeds the plagiarism threshold
                if similarity > plag:
                    plagiarized_files.append(
                        (file1_path, file2_path, similarity))

        # Generate the result message
        if len(plagiarized_files) > 0:
            message = "Plagiarized files:\n\n"
            for file1, file2, similarity in plagiarized_files:
                message += f"{file1} and {file2}: {similarity}% similarity\n"
        else:
            message = "No plagiarized files"

        messagebox.showinfo("Plagiarism Checker", message)

    # Create a new window for the folder comparison
    comparison_window = tk.Toplevel(window)
    comparison_window.title("Compare All Files in Folder")

    # Create and place the GUI elements
    label_percentage = tk.Label(
        comparison_window, text="Enter the percentage of plagiarism allowed:")
    label_percentage.pack()

    percentage_entry = tk.Entry(comparison_window)
    percentage_entry.pack()

    # Variable to store the folder path
    folder_path_var = tk.StringVar()

    button_browse_folder = tk.Button(
        comparison_window, text="Browse Folder", command=lambda: browse_folder_path(folder_path_var))
    button_browse_folder.pack()

    button_compare = tk.Button(
        comparison_window, text="Compare", command=perform_comparison)
    button_compare.pack()

    comparison_window.mainloop()


# UTILITY FUNCTIONS

def browse_folder_path(folder_path_var):
    # Browse and select the folder path
    folder_path = filedialog.askdirectory()
    folder_path_var.set(folder_path)


def browse_masterfile_path(masterfile_path_var):
    # Browse and select the masterfile path
    masterfile_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")])
    masterfile_path_var.set(masterfile_path)


def browse_file1_path(file1_path_var):
    # Browse and select the path of the first file
    file1_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")])
    file1_path_var.set(file1_path)


def browse_file2_path(file2_path_var):
    # Browse and select the path of the second file
    file2_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")])
    file2_path_var.set(file2_path)


# Create the main GUI window
window = tk.Tk()
window.title("Plagiarism Checker")
window.geometry("400x300")

# Create GUI elements
label = tk.Label(window, text="Choose an option:")
label.pack()

# Option 1: Compare folder with masterfile
# button_folder_master = tk.Button(
#  window, text=" , command=compare_folder_with_masterfile)
# button_folder_master.pack()

# Option 2: Compare two files
button_two_files = tk.Button(
    window, text="Compare Two Files", command=compare_two_files)
button_two_files.pack()

# Option 3: Compare all files in a folder
# button_all_files = tk.Button(
#     window, text="Compare All Files in Folder", command=compare_all_files_in_folder)
# button_all_files.pack()

# Exit button
button_exit = tk.Button(window, text="Exit", command=window.quit)
button_exit.pack()

# Run the GUI
window.mainloop()
