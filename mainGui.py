'''
This function implements the GUI side of the entire Graph-Based Recommendation
system. The design is such that main features such as:
Parental Control => Add keyword
Search by title (e.g The God of High School)
search by Genre (e.g Comedy, TV)
search by Year (e.g 2019)
'''

from Knowledge_Graph import KnowledgeGraph
from movie_filtering import process_dataset
from recommender import recommender_system, get_movie_info_display, retrieve_default_lists
import tkinter as tk
from tkinter import simpledialog
import random

#create instances of the custom classes
PD = process_dataset()
KG = KnowledgeGraph()
all_movies_KG = KG.Graph_all_movies()

#create call back functions
def add_keyword():

    global all_movies_KG
    user_input = simpledialog.askstring("Parental COntrol","enter an unacceptable word to filter out.")

    done = PD.update_list(str(user_input))
    if done == True:
        PD.process_file()
        all_movies_KG = KG.Graph_all_movies()
        stringVal = str(user_input)+' '+'successfuly added!'
        result_text.delete("1.0", "end")
        result_text.insert(tk.END, stringVal)



#create functions to get movie parameters
def get_title():
    stringVal = ''
    user_input = simpledialog.askstring("search movies by title", "enter the movie name to search for")
    movies_list, movies_found = recommender_system('movie_name', user_input, all_movies_KG)
    if movies_found == True:
        stringVal += 'Here is the movie based on your search:'+'\n'
        stringVal += '\n'
        stringVal += get_movie_info_display(movies_list)
    else:
        stringVal += 'There are no matches to name search: Here are some recommendations for you:'+'\n'
        stringVal += '\n'
        stringVal+= get_movie_info_display(movies_list)

    result_text.delete("1.0", "end")
    result_text.insert(tk.END, stringVal)


def get_genre():
    stringVal = ''
    user_input = simpledialog.askstring("search movies by Genre", "enter the genre to search for")
    movies_list, movies_found = recommender_system('genre', user_input, all_movies_KG)
    if movies_found == True:
        stringVal += 'Here is the movie based on your search:' + '\n'
        stringVal += '\n'
        stringVal += get_movie_info_display(movies_list)
    else:
        stringVal += 'There are no matches to genre search: Here are some recommendations for you:' + '\n'
        stringVal += '\n'
        stringVal += get_movie_info_display(movies_list)

    result_text.delete("1.0", "end")
    result_text.insert(tk.END, stringVal)


def get_year():
    stringVal = ''
    user_input = simpledialog.askstring("search movies by title", "enter the movie name to search for")
    movies_list, movies_found = recommender_system('year', user_input, all_movies_KG)
    if movies_found == True:
        stringVal += 'Here is the movie based on your search:' + '\n'
        stringVal += '\n'
        stringVal += get_movie_info_display(movies_list)
    else:
        stringVal += 'There are no matches to year search: Here are some recommendations for you:' + '\n'
        stringVal += '\n'
        stringVal += get_movie_info_display(movies_list)

    result_text.delete("1.0", "end")
    result_text.insert(tk.END, stringVal)


def get_default_lists():
    #displays up to 20 top movies for your pick
    stringVal = 'Top latest movies to put on your watch list'+'\n'
    stringVal += '\n'
    movie_years = ['2015','2016','2017', '2018', '2020', '2019']

    yr = random.choice(movie_years)
    movies_list = retrieve_default_lists(all_movies_KG, yr)
    stringVal += get_movie_info_display(movies_list)

    yr = random.choice(movie_years)
    movies_list = retrieve_default_lists(all_movies_KG, yr)
    stringVal += get_movie_info_display(movies_list)

    yr = random.choice(movie_years)
    movies_list = retrieve_default_lists(all_movies_KG, yr)
    stringVal += get_movie_info_display(movies_list)

    yr = random.choice(movie_years)
    movies_list = retrieve_default_lists(all_movies_KG, yr)
    stringVal += get_movie_info_display(movies_list)


    return stringVal


#create the GUI instance
menu_window = tk.Tk()
menu_window.geometry("960x800")
menu = tk.Menu(menu_window)
menu_window.config(menu=menu)
Parental_control_menu = tk.Menu(menu)
menu.add_cascade(label='Parent Control', menu=Parental_control_menu)
Parental_control_menu.add_command(label='Add Keyword', command=add_keyword)
Parental_control_menu.add_command(label='Exit', command=menu_window.quit)

Movie_search_menu = tk.Menu(menu_window)
menu.add_cascade(label='search for movies', menu=Movie_search_menu)
Movie_search_menu.add_command(label='search by title', command=get_title)
Movie_search_menu.add_command(label='search by genre', command=get_genre)
Movie_search_menu.add_command(label='search by year', command=get_year)
Movie_search_menu.add_command(label='Exit', command=menu_window.quit)

#create lable widget to display all results
stringVal = get_default_lists()
#result_label = tk.Label(menu_window, text=stringVal, wraplength=900, font='8')
#result_label.pack()

result_text = tk.Text(menu_window, width=600, height=700, wrap=tk.WORD)
scrollbar = tk.Scrollbar(menu_window)
result_text.configure(yscrollcommand=scrollbar.set)
result_text.pack(side=tk.LEFT)

scrollbar.config(command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text.insert(tk.END, stringVal)




tk.mainloop()

