import itertools


class Book:
  def __init__(self, book_id, score):
   self.book_id = int(book_id)
   self.score = int(score)
   self.scanned = False

  def __str__(self):
    return '  Book id {} has score {}'.format(self.book_id, self.score)

  def is_scanned(self):
    return self.scanned


class Library:
  def __init__(self, lib_id, nb, signup, shiped, book_collection):
    self.library_id = int(lib_id)
    self.nb_of_books = int(nb)
    self.signup_process_days = int(signup)
    self.nb_shiped_by_day = int(shiped)
    self.book_collection = book_collection
    # sort books by score descending
    self.book_collection.sort(key=lambda x: x.score, reverse=True)
    self.books_not_scanned = []
    self.chunked_book_collection = []


  def __str__(self):
    return '  Library id {} has {} books, takes {} days to signup, can ship {} per day'.format(
      self.library_id,
      self.nb_of_books,
      self.signup_process_days,
      self.nb_shiped_by_day
    )


def read_input(filename):
  with open(filename, 'r') as input_file:
    BOOK_NB, LIBRARY_NB, DAYS = [int(v) for v in input_file.readline().split(' ')]
    BOOKS = [int(v) for v in input_file.readline().split(' ')]

    # print(BOOK_NB)
    # print(LIBRARY_NB)
    # print(DAYS)

    library_counter = 0
    libraries = []
    for line in range(LIBRARY_NB):
      N_nb_of_book, T_sign_up_process_days, M_nb_shiped_per_day = [int(v) for v in input_file.readline().split(' ')]
      book_collection = [Book(int(v), BOOKS[int(v)]) for v in input_file.readline().split(' ')]

      this_library = Library(library_counter, N_nb_of_book, T_sign_up_process_days, M_nb_shiped_per_day, book_collection)

      # print(N_nb_of_book + T_sign_up_process_days + M_nb_shiped_per_day)
      # print(book_collection)

      libraries.append(this_library)
      library_counter += 1

    # print(libraries)

    return (BOOK_NB, LIBRARY_NB, DAYS, libraries)


def write_output(output_filename, output):
  '''
  nb library a sign up

  <section>
  id de la lib + nb books
  list de book id
  </section>
  '''
  nice_output = '{}\n'.format(output.pop(0))
  for sections in output:
    for line in sections:
      nice_output += '{}\n'.format(' '.join([str(v) for v in line]))

  with open(output_filename, 'w') as output_file:
    output_file.write(nice_output)


def solve(input_data):
  total_book_number = input_data[0]
  total_number_of_libraries = input_data[1]
  remaining_days = int(input_data[2])
  libraries = input_data[3]

  print('START = there are {} total days\n'.format(remaining_days))
  nb_library = 0
  sections = []
  for library in libraries:
    nb_library += 1
    if int(library.signup_process_days) > remaining_days:
      continue
    print(library)

    remaining_days -= int(library.signup_process_days)
    print('- ITER = there are {} days remaining'.format(remaining_days))

    # on coupe le book_collection non-scanné en groupe de books/jour
    # et on garde remaining_days de chunks
    library.books_not_scanned = list(
      filter(lambda x: not x.scanned, library.book_collection))
    # print(list(map(lambda x: x.book_id, library.books_not_scanned)))

    library.chunked_book_collection = [
      library.books_not_scanned[i * library.nb_shiped_by_day:(i + 1) * library.nb_shiped_by_day]
      for i in range((len(library.books_not_scanned) + library.nb_shiped_by_day - 1) // library.nb_shiped_by_day)]
    # print(library.chunked_book_collection)

    books_to_send = library.chunked_book_collection[:remaining_days]
    # print(books_to_send)

    flatten_books = list(itertools.chain(*books_to_send))
    nb_of_books_to_send = len(flatten_books)
    # print(nb_of_books_to_send)

    library_score = 0
    for book in flatten_books:
      library_score += int(book.score)
      book.scanned = True
    # print(library_score)

    sections.append([
      [library.library_id, len(flatten_books)],
      [v.book_id for v in flatten_books]
    ])

  print('\nFINISH = there are {} days remaining'.format(remaining_days))

  return [
    nb_library,
    *sections
  ]


if __name__ == "__main__":
  input_filename = 'input/a_example.txt'
  output_filename = input_filename.replace('in', 'out')

  input_data = read_input(input_filename)
  output = solve(input_data)
  print()

  write_output(output_filename, output)
