README.txt for clarkeWright.py
Written by Group 26: Morgan Brenner, Sammy Pettinichi, Rachel Weissman-Hohler
Last modified: 12/2/16

Set-up: 
Place clarkeWright.py in the same directory as the problem text file.

Execute:
Enter "python clarkeWright.py <problem-file-name> [-l]" (without the quotation marks) into the command line to run the program on the given problem file. The -l argument is optional. If you use the -l flag, the program will limit the running time for the 2-Opt portion of the solver to 160 seconds. This will insure that the 2-Opt doesn't make the running time go over 180 seconds. However, if the problem is large enough, the running time could go over the 160 seconds just during the Clarke-Wright portion. The -l will not stop the program before it has found a solution. If you omit the -l flag, the program will be limited to 7200 seconds (plus some time to finish the final loop of 2-Opt and print the results to file), which is significantly more than enough to find this solver's most optimal solution to the provided problems.

Results:
Once the program has completed, it will write the results to a file named <problem-file-name>.tour and print the time the program took to execute to stdout. 

Example execution:
-bash-4.2$ python clarkeWright.py tsp_example_1.txt
0.0564889907837 seconds
-bash-4.2$ 