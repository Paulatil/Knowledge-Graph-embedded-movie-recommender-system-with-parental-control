'''
this program ranks movie recommendations based on the different inputs
received
'''
import networkx as Graph
import random


def recommender_system(search_term, search_word, movie_KG):

    movie_name = ''
    movie_genres = list()
    movie_synopsis = ''
    movie_year = ''
    movie_rating = ''
    movies_list = dict()

    #search by title
    if search_term == 'movie_name':
        if search_word in movie_KG:
            movie_name = search_word
            movie_params = dict()
            edge_labels = Graph.get_edge_attributes(movie_KG, 'movie')
            for keys, value in edge_labels.items():
                if search_word == keys[0]:
                    if value == 'genre':
                        movie_genres.append(keys[1])
                    elif value == 'Released in':
                        movie_year = keys[1]
                    elif value == 'rating of':
                        movie_rating = keys[1]
                    elif value == 'synopsys':
                        movie_synopsis = keys[1]

            movie_params['genres'] = movie_genres
            movie_params['year'] = movie_year
            movie_params['synopsis'] = movie_synopsis
            movies_list[movie_name] = movie_params
            movie_found = True
            return movies_list, movie_found

        else:
            movies_list = retrieve_top_movies(movie_KG)
            movie_found = False
            return movies_list, movie_found

    #search by genre
    elif search_term == 'genre':
        if search_word in movie_KG:
            movies_list = retrieve_genre_movies(movie_KG, search_word)
            genre_found = True
            return movies_list, genre_found

        else:
            movies_list = retrieve_top_movies(movie_KG)
            genre_found = False
            return movies_list, genre_found

    #search by year
    elif search_term == 'year':
        if search_word in movie_KG:
            movies_list = retrieve_year_movies(movie_KG, search_word)
            year_found = True
            return movies_list, year_found

        else:
            movies_list = retrieve_top_movies(movie_KG)
            year_found = False
            return movies_list, year_found




#retireve top 5 movies when name, genre, year,
def retrieve_top_movies(movie_KG):
    edge_labels = Graph.get_edge_attributes(movie_KG, 'movie')
    movies_list = dict()

    for keys, value in edge_labels.items():
        if value == 'rating of':
            rating = float(keys[1])
            if rating > 7.0:
                genres = list()
                movie_detail = dict()
                synopsis = ''
                year = ''
                movie_name = keys[0]
                for mn, gen in edge_labels.items():
                    if mn[0] == movie_name:
                        if gen == 'genre':
                            genres.append(mn[1])
                        elif gen == 'Released in':
                            year = mn[1]
                        elif gen == 'synopsys':
                            synopsis = mn[1]
                movie_detail['genres'] = genres
                movie_detail['year'] = year
                movie_detail['synopsys'] = synopsis
                movies_list[movie_name] = movie_detail

    #randomly select top 5 movies
    if len(movies_list) > 5:
        top_list = dict()

        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details

        return top_list

    else:
        return movies_list



#retrieve top 5 movies with genre
def retrieve_genre_movies(movie_KG, search_word):
    edge_labels = Graph.get_edge_attributes(movie_KG, 'movie')

    movies_list = dict()

    for keys, value in edge_labels.items():
        if value == 'genre':
            if search_word == keys[1]:
                movie_name = keys[0]
                movie_params = dict()
                movie_genres = list()
                year = ''
                synopsis = ''

                for mn, val in edge_labels.items():
                    if movie_name == mn[0]:
                        if val == 'genre':
                            movie_genres.append(mn[1])
                        elif val == 'Released in':
                            year = mn[1]
                        elif val == 'synopsys':
                            synopsis = mn[1]
                movie_params['genres'] = movie_genres
                movie_params['year'] = year
                movie_params['synopsys'] = synopsis

                movies_list[movie_name] = movie_params

    #randomly select any 5 movies from list

    if len(movies_list) > 5:
        top_list = dict()

        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details

        return top_list

    else:
        return movies_list



#retrieve top 5 movies with year
def retrieve_year_movies(movie_KG, search_word):
    edge_labels = Graph.get_edge_attributes(movie_KG, 'movie')

    movies_list = dict()

    for keys, value in edge_labels.items():
        if value == 'Released in':
            if search_word == keys[1]:
                movie_name = keys[0]
                movie_params = dict()
                movie_genres = list()
                year = ''
                synopsis = ''

                for mn, val in edge_labels.items():
                    if movie_name == mn[0]:
                        if val == 'genre':
                            movie_genres.append(mn[1])
                        elif val == 'Released in':
                            year = mn[1]
                        elif val == 'synopsys':
                            synopsis = mn[1]
                movie_params['genres'] = movie_genres
                movie_params['year'] = year
                movie_params['synopsys'] = synopsis

                movies_list[movie_name] = movie_params

    # randomly select any 5 movies from list

    if len(movies_list) > 5:
        top_list = dict()

        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        #movie_name, movie_details = random.sample(list(movies_list.items()), 1)
        #top_list[movie_name] = movie_details


        return top_list

    else:
        return movies_list


#get movie lists and its properties
def get_movie_info(movies_list):

    if type(movies_list) == dict:
        for name, params in movies_list.items():
            if type(params) == dict:
                movie_genres = ''
                movie_year = ''
                movie_synopsys = ''
                for param_name, param_val in params.items():
                    if param_name == 'genres':
                        for genre in param_val:
                            movie_genres += str(genre) +", "
                    elif param_name == 'year':
                        movie_year = param_val
                    elif param_name == 'synopsys':
                        movie_synopsys = param_val

                print('=================================')
                print('Movie Name: {}'.format(name))
                print('Movie Genre(s): {}'.format(movie_genres))
                print('Released in: {}'.format(movie_year))
                print('Synopsis: {} \n'.format(movie_synopsys))


#default movie list
def retrieve_default_lists(movie_KG, year):
    edge_labels = Graph.get_edge_attributes(movie_KG, 'movie')

    movies_list = dict()

    for keys, value in edge_labels.items():
        if value == 'Released in':
            if year == keys[1]:
                movie_name = keys[0]
                movie_params = dict()
                movie_genres = list()
                year = ''
                synopsis = ''

                for mn, val in edge_labels.items():
                    if movie_name == mn[0]:
                        if val == 'genre':
                            movie_genres.append(mn[1])
                        elif val == 'Released in':
                            year = mn[1]
                        elif val == 'synopsys':
                            synopsis = mn[1]
                movie_params['genres'] = movie_genres
                movie_params['year'] = year
                movie_params['synopsys'] = synopsis

                movies_list[movie_name] = movie_params

    # randomly select any 5 movies from list

    if len(movies_list) > 3:
        top_list = dict()

        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        movie_name, movie_details = random.choice(list(movies_list.items()))
        top_list[movie_name] = movie_details
        #movie_name, movie_details = random.choice(list(movies_list.items()))
        #top_list[movie_name] = movie_details
        #movie_name, movie_details = random.choice(list(movies_list.items()))
        #top_list[movie_name] = movie_details
        #movie_name, movie_details = random.choice(list(movies_list.items()))
        #top_list[movie_name] = movie_details
        #movie_name, movie_details = random.choice(list(movies_list.items()))
        #top_list[movie_name] = movie_details

        return top_list

    else:
        return movies_list


def get_movie_info_display(movies_list):

    stringVal = ''

    if type(movies_list) == dict:
        for name, params in movies_list.items():
            if type(params) == dict:
                movie_genres = ''
                movie_year = ''
                movie_synopsys = ''
                for param_name, param_val in params.items():
                    if param_name == 'genres':
                        for genre in param_val:
                            movie_genres += str(genre) +", "
                    elif param_name == 'year':
                        movie_year = param_val
                    elif param_name == 'synopsys':
                        movie_synopsys = param_val

                stringVal += 'Name:'+' '+str(name)+'\n'
                stringVal += 'Genre(s):'+' '+ movie_genres +'\n'
                stringVal += 'Released in:'+' '+ movie_year +'\n'
                stringVal += 'synopsis:'+' '+ movie_synopsys +'\n'
                stringVal += '\n'

    return stringVal
















