'''
This file contains the implementation of knowledge graph built from the processed data output from
movie_filtring.py program. This structures the data such that each movie candidate for the recommender system
is identified by some properties such as the genre, year, studio, synopsis, title, and rating
'''

import csv
import numpy as np
import matplotlib.pyplot as plt
import networkx as Graph
import scipy

class KnowledgeGraph():
    """
    All graph related codes are implemented here
    """

    #this function plots all movie title and genres as nodes with edges linking each
    def Graph_all_movies(self):
        """
        This plots the full DiGraph of all movies showing their similarities around genres, and ratings
        """

        all_movies = Graph.MultiDiGraph()

        read_genres = list()
        genres_colors = ['#5013ED', '#42853C', '#D4E907', '#2A257D',
                        '#EF093B', '#8CA030', '#35B1DA', '#3F4F33',
                        '#CAA341', '#B69BAE', '#E77FE2', '#9483F4',
                        '#77DF5D', '#F3902F', '#E88182', '#713338',
                        '#5CEFAB', '#863771', '#53EF26', '#FF80FF', '#6FF6FF',
                        '#B0171F', '#FFB6C1', '#FF69B4', '#BA55D3', '#9FB6CD',
                        '#96CDCD', '#4EEE94', '#CDCDB4', '#FFB90F', '#FFE4C4']
        movie_years_colors = ['#CAA341', '#B69BAE', '#E77FE2', '#9483F4', '#B0171F',
                              '#FFB6C1', '#FF69B4', '#BA55D3', '#9FB6CD',]
        movie_rating_colors = ['#B0171F', '#FFB6C1', '#FF69B4', '#BA55D3', '#9FB6CD',
                                '#96CDCD', '#4EEE94', '#CDCDB4', '#FFB90F', '#FFE4C4']
        movie_synopsis_colors = ['#5013ED', '#42853C', '#D4E907', '#2A257D',
                                 '#96CDCD', '#4EEE94', '#CDCDB4', '#FFB90F', '#FFE4C4',
                                 '#5CEFAB', '#863771', '#53EF26', '#FF80FF', '#6FF6FF']
        movie_synopsis_color = dict()
        movie_rating_color = dict()
        movie_year_color = dict()
        genres_color = dict()
        movies_genres = dict()
        color_map = list()

        #get the Q_movies list from movie_filtering output
        with open('Q_AnimeWorld.csv', encoding="utf8") as movie_list:
            get_movies = csv.reader(movie_list, delimiter=',')

            get_movies = list(filter(None, get_movies))
            for m_list in get_movies:
                all_movies.add_node(m_list[1])           # add a movie title as a node
                #color_map.append('Green')
                title = m_list[1]
                genres = m_list[2].split(", ")
                p_genres = list()
                for genre in genres:
                    genre = genre.lstrip('\[')
                    genre = genre.lstrip("\'")
                    genre = genre.rstrip("\'")
                    genre = genre.rstrip('\]')
                    genre = genre.rstrip("\'")
                    p_genres.append(genre)

                if len(p_genres) == 1:
                    content = p_genres[0]
                    if not content:
                        p_genres[0] = 'TV'
                movies_genres[title] = p_genres
                #print('genre list {}: length {}'.format(p_genres, len(p_genres)))

                #add genres to graph nodes
                for genre in p_genres:
                    if genre not in all_movies:
                        all_movies.add_node(genre)
                        read_genres.append(genre)
                        gcolor = genres_colors[len(genres_color)%31]
                        genres_color[genre] = gcolor
                        #color_map.append(gcolor)
                    all_movies.add_edge(title, genre, movie='genre')

                #add movie year to graph
                movie_year = m_list[5]
                if not movie_year:
                    movie_year = '2019'

                if movie_year not in all_movies:
                    all_movies.add_node(movie_year)
                    ycolor = movie_years_colors[len(movie_year_color)%9]
                    movie_year_color[movie_year] = ycolor
                    #color_map.append(ycolor)
                all_movies.add_edge(title, movie_year, movie='Released in')

                #add movie rating to graph
                movie_rating = m_list[6]
                if not movie_rating:
                    movie_rating = '6.0'

                if movie_rating not in all_movies:
                    all_movies.add_node(movie_rating)
                    rcolor = movie_rating_colors[len(movie_rating_color)%9]
                    movie_rating_color[movie_rating] = rcolor
                    #color_map.append(rcolor)
                all_movies.add_edge(title, movie_rating, movie='rating of')


                #add synopsis to graph
                movie_synopsis = m_list[3]
                if not movie_synopsis:
                    movie_synopsis = 'No movie description'

                if movie_synopsis not in all_movies:
                    all_movies.add_node(movie_synopsis)
                    scolor = movie_synopsis_colors[len(movie_synopsis_color)%13]
                    movie_synopsis_color[movie_synopsis] = scolor
                    #color_map.append(scolor)
                all_movies.add_edge(title, movie_synopsis, movie='synopsys')



        #get edge colors and node colors
        #merge all colors into one structure
        all_colors = {**genres_color, **movie_year_color, **movie_rating_color, **movie_synopsis_color}
        #print(len(all_colors))

        edge_colors =list()
        for edge in all_movies.edges:
            #print(edge[1])
            edge_color = all_colors[edge[1]]
            edge_colors.append(edge_color)


        #print(len(edge_colors))

        for node in all_movies:
            if node in read_genres:
                color_map.append('blue')
            elif node in movies_genres:
                hex_ = [all_colors[gen] for gen in movies_genres[str(node)]]
                avg_color = sum(list(map(lambda x: int(x[1:], 16), hex_)))//len(hex_)
                average_color = f'#{avg_color:06x}'
                color_map.append(average_color)
            else:
                hex_ = all_colors[str(node)]
                #hex_c = f'#{hex_:06x}'
                color_map.append(hex_)


        #print(len(color_map))
        edge_label = Graph.get_edge_attributes(all_movies, 'movie')
        #print(edge_label)


        '''
        plt.figure(figsize=(150,150))
        positions = Graph.spring_layout(all_movies, k=1.0, iterations=20)
        Graph.draw(all_movies, with_labels=True, node_color=color_map, edge_color=edge_colors, node_size=4500,
                   edge_cmap=plt.cm.Blues, font_size=16, pos=positions)
        edge_label = Graph.get_edge_attributes(all_movies, 'movie')

        new_edge_label = dict()
        for key, val in edge_label.items():
            new_key = key[:-1]
            new_edge_label[new_key] = val
        #print(new_edge_label.keys())
        Graph.draw_networkx_edge_labels(all_movies, pos=positions, edge_labels=new_edge_label, font_size=16)
        plt.savefig("movies_graph.png")
        plt.show()
        '''

        return all_movies


    # this function shoes a plot of the details of each movie: genre, synopsis, year, ratings, and title
    def Graph_movie_details(self, movie_title):
        curr_movie = Graph.MultiDiGraph()

        color_map = list()
        colors = ['#5013ED', '#42853C', '#D4E907', '#2A257D', '#EF093B', '#8CA030']
        node_size = list()


        #read the csv file
        with open('Q_AnimeWorld.csv', encoding="utf8") as movie_list:
            get_movies = csv.reader(movie_list, delimiter=',')

            get_movies = list(filter(None, get_movies))    #remove empty rows
            for m_list in get_movies:
                if m_list[1] == movie_title:
                    a = m_list[1]
                    curr_movie.add_node(m_list[1])
                    color_map.append('Green')        #color of node
                    node_size.append(20000)          #size of node

                    if not m_list[5]:
                        m_list[5] = "2019"
                    curr_movie.add_node(m_list[5])   #add movie year
                    color_map.append(colors[0])
                    node_size.append(10000)
                    curr_movie.add_edge(m_list[1], m_list[5], movie='Released in')

                    curr_movie.add_node(m_list[3])     #add movie synopsis
                    color_map.append(colors[1])
                    node_size.append(10000)
                    curr_movie.add_edge(m_list[1], m_list[3], movie='Synopsis')

                    if not m_list[6]:
                        m_list[6] = '1.0'
                    curr_movie.add_node(m_list[6])   #add ratings
                    color_map.append(colors[2])
                    node_size.append(10000)
                    curr_movie.add_edge(m_list[1], m_list[6], movie='has a rating of')

                    curr_movie.add_node("Genres")
                    color_map.append(colors[3])
                    node_size.append(10000)
                    curr_movie.add_edge(m_list[1], "Genres", movie='Genres include')


                    if not m_list[2]:
                        genres = ['TV']
                    else:
                        genres = list(m_list[2].split(", "))


                    for genre in genres:
                        genre = genre.lstrip('\[')
                        genre = genre.lstrip("\'")
                        genre = genre.rstrip("\'")
                        genre = genre.rstrip('\]')
                        genre = genre.rstrip("\'")

                        curr_movie.add_node(genre)
                        color_map.append(colors[4])
                        node_size.append(5000)
                        curr_movie.add_edge("Genres", genre)

        plt.figure(figsize=(25,25))
        position = Graph.shell_layout(curr_movie)
        position[a] = np.array([0,0])
        Graph.draw(curr_movie, with_labels=True, node_color=color_map, node_size=node_size, edge_cmap=plt.cm.Blues, font_size=20, pos=position)
        edge_label = Graph.get_edge_attributes(curr_movie, 'movie')



        new_edge_label = dict()
        for key, val in edge_label.items():
            new_key = key[:-1]
            new_edge_label[new_key] = val
        print(new_edge_label.keys())
        Graph.draw_networkx_edge_labels(curr_movie, pos=position, edge_labels=new_edge_label, font_size=20)
        plt.savefig("movie_detail.png")
        plt.show()



    #plot a similarity graph between two movies comparism
    def Graph_similarity(self, movie1, movie2):
        curr_movies = Graph.MultiDiGraph()
        color_map = list()
        node_size = list()
        colors = ['#5013ED', '#42853C', '#D4E907', '#2A257D']
        b = ''

        # read the csv file
        with open('Q_AnimeWorld.csv', encoding="utf8") as movie_list:
            get_movies = csv.reader(movie_list, delimiter=',')

            get_movies = list(filter(None, get_movies))  # remove empty eows
            for m_list in get_movies:
                if m_list[1] == movie1:
                    a = m_list[1]
                    movie_1 = m_list[1]
                    break

        # read the csv file
        with open('Q_AnimeWorld.csv', encoding="utf8") as movie_list:
            get_movies = csv.reader(movie_list, delimiter=',')

            get_movies = list(filter(None, get_movies))  # remove empty rows
            for m_list in get_movies:
                if m_list[1] == movie2:
                    b = m_list[1]

                    curr_movies.add_node(m_list[1])         #add movie2's title
                    color_map.append(colors[0])
                    node_size.append(20000)

                    curr_movies.add_node(movie_1[1])      #add movie1's title
                    color_map.append(colors[0])
                    node_size.append(20000)


                    if not m_list[2]:
                        m_list[2] = 'TV'
                    genre_list = list(m_list[2].split(", "))
                    for genre in genre_list:
                        if genre not in curr_movies:
                            curr_movies.add_node(genre)
                            color_map.append(colors[1])
                            node_size.append(10000)
                        curr_movies.add_edge(m_list[1], genre, movie='Genre')

                    if not movie_1[2]:
                        movie_1[2] = 'TV'
                    genre_list = list(movie_1[2].split(", "))
                    for genre in genre_list:
                        if genre not in curr_movies:
                            curr_movies.add_node(genre)                         #add genres
                            color_map.append(colors[1])
                            node_size.append(10000)
                        curr_movies.add_edge(movie_1[1], genre, movie='Genre')


                    if not m_list[5]:
                        m_list[5] = 2019
                    curr_movies.add_node(m_list[5])               #add year
                    color_map.append(colors[2])
                    node_size.append(10000)
                    curr_movies.add_edge(m_list[1], m_list[5], novie='Released in')

                    if not movie_1[5]:
                        movie_1[5] = 2019
                    curr_movies.add_node(movie_1[5])
                    color_map.append(colors[2])
                    node_size.append(10000)
                    curr_movies.add_edge(movie_1[1], movie_1[5], movie='Released in')


                    if not m_list[6]:
                        m_list[6] = 1.0
                    curr_movies.add_node(m_list[6])            #add ratings
                    color_map.append(colors[3])
                    node_size.append(10000)
                    curr_movies.add_edge(m_list[1], m_list[6], movie='Rating')

                    if not movie_1[6]:
                        movie_1[6] = 1.0
                    curr_movies.add_node(movie_1[6])
                    color_map.append(colors[3])
                    node_size.append(10000)
                    curr_movies.add_edge(movie_1[1], movie_1[6], movie='Rating')


        plt.figure(figsize=(35,35))
        position = Graph.planar_layout(curr_movies)
        position[a] = np.array([1,0])
        position[b] = np.array([-1,0])
        Graph.draw(curr_movies, with_labels=True, node_color=node_size, edge_cmap=plt.cm.Blues, font_size=10, pos=position)
        edge_label = Graph.get_edge_attributes(curr_movies, 'movie')
        new_edge_label = dict()
        for key, val in edge_label.items():
            new_key = key[:-1]
            new_edge_label[new_key] = val
        #print(new_edge_label.keys())
        Graph.draw_networkx_edge_labels(curr_movies, position, edge_labels=new_edge_label, font_size=20)
        plt.savefig('comparism.png')
        plt.show()








#check code functionality
#KG = KnowledgeGraph()

#movie_KG = KG.Graph_all_movies()
#KG.Graph_movie_details('Yakusoku no Neverland')
#KG.Graph_similarity('Kabukichou Sherlock','Chihayafuru 3')








