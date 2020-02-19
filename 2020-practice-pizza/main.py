class Hashcode2020:
  MAX_PIZZA = 0
  NUMBER_TYPE_PIZZA = 0
  input_filename = 'input/a_example.in'
  output_filename = input_filename.replace('in', 'out')

  def read_input(self):
    with open(self.input_filename, 'r') as input_file:
      self.MAX_SLICES, self.NUMBER_TYPE_PIZZA = input_file.readline().split(' ')
      return [int(v) for v in input_file.readline().split()]

  def solve(self, input):
    solution = []
    score = 0

    i = len(input) - 1
    solved, keep_going = False, True
    while(i > 0 and not solved):
      tmp_solution = []
      j = i
      sum_slices = 0

      while(j >= 0 and keep_going):
        current_pizza = input[j]
        if (sum_slices + current_pizza < int(self.MAX_SLICES)):
            sum_slices += current_pizza
            tmp_solution.append(j)
        elif (sum_slices + current_pizza == int(self.MAX_SLICES)):
            sum_slices += current_pizza
            tmp_solution.append(j)
            solved, keep_going = True, False
        j -= 1

      if (score < sum_slices):
        score = sum_slices
        solution = tmp_solution
      if (len(solution) == len(input)):
        solved = True
      i -= 1

    solution.reverse()
    return solution 

  def write_output(self, output):
    with open(self.output_filename, 'w') as output_file:
      output_file.write(str(len(output)) + '\n')
      output_file.write(' '.join([str(v) for v in output]))


if __name__ == "__main__":
  hashcode = Hashcode2020()
  input = hashcode.read_input()
  print('Max slices: {}'.format(hashcode.MAX_SLICES))
  print('Number of pizza types: {}'.format(hashcode.NUMBER_TYPE_PIZZA))
  print('input: {}'.format(input))

  output = hashcode.solve(input)
  print('output: {}\n'.format(output))

  hashcode.write_output(output)
  print('Solved number of slices: {}'.format(
    sum([input[v] for v in output])))

