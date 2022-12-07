'''
  The movie filtering mechanism allows restrictions to what certain movies can be recommended.
  This entails analysing the short synopsis of a movie for certain buzz words that detail the content
  of the movie. Thorough analyses would be to retrieve the full transcript of a movie to examine closely
  if it meets the selection criteria of movie candidates for recommendation.
'''
import csv
import string

unacceptable_words = ['fuck','nude','sex','armsdeal','voilence','rape','fornicate','adultery','gay',
                      'lesbian','gun','drugs','cocain','stupid','ass','jerk','x-rated','naked','incest',
                      'nuclear','war head','bomb','boobs','dick','masturbate']

threshold = 0.2    #acceptable threshold above which a movie does not qualify as candidate movie

class process_dataset():
    """
    dataset are read and processed for any stop words within the context of voilence and vulgar.
    This filters out the candidate movies that can be fed into the knowledge graph system
    """

    def process_file(self):

        Q_animeworld = list()       #retrieve qualified candidate movies for knowledge graph

        with open('AnimeWorld.csv', encoding="utf8") as file:

            #read the CVS file
            csvfile = csv.reader(file, delimiter=',')

            line_count = 0

            for line in csvfile:
                if line_count == 0:    #skip header
                    line_count = 1
                    continue

                #process movie synopsis to check for unacceptable words
                synopsis = line[4].translate(str.maketrans('','',string.punctuation))
                description = list(synopsis.split(" "))

                #check for unacceptable words
                word_count = 0
                for word in unacceptable_words:
                    word_count += description.count(word)

                if float(word_count/100) < threshold:
                    yr = list(line[5].split(","))
                    if len(yr) > 1:
                        line[5] = str(yr[1].replace(" ",""))
                        #print(str(yr[1].replace(" ","")))
                    elif len(yr) == 1:
                        yr = list(yr[0].split(" "))
                        #print(str(yr[1]))
                        line[5] = str(yr[1])

                        #print(line[5])
                    Q_animeworld.append(line)

                line_count += 1

        with open('Q_AnimeWorld.csv', mode='w', encoding="utf8") as write_file:
            csv_writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for q_line in Q_animeworld:
                if len(q_line) > 0:
                    csv_writer.writerow(q_line)

    # function to append keywords to list of unacceptable words
    def update_list(self, keyword):
        unacceptable_words.append(str(keyword))
        if keyword in unacceptable_words:
            done = True
            print('"{}" was successfully added \n'.format(keyword))
        return done



















"""
 Test run for check
"""
#read_in = process_dataset()

#read_in.process_file()








