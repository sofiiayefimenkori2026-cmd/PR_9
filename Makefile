CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

PROGRAMS = Lab_09_1 Lab_09_2_1_b1 Lab_09_2_1_b2
TESTS = tests/UnitTest_09_1 tests/UnitTest_09_2_1

.PHONY: all programs tests test check clean help

all: programs tests

programs: $(PROGRAMS)

Lab_09_1: PR_9.1/var.cpp PR_9.1/dod.cpp PR_9.1/sum.cpp PR_9.1/Lab_09_1.cpp PR_9.1/var.h PR_9.1/dod.h PR_9.1/sum.h
	$(CXX) $(CXXFLAGS) -IPR_9.1 PR_9.1/var.cpp PR_9.1/dod.cpp PR_9.1/sum.cpp PR_9.1/Lab_09_1.cpp -o $@

Lab_09_2_1_b1: PR_9.2_1/Lab_09_2_1.cpp PR_9.2_1/macros.h
	$(CXX) $(CXXFLAGS) -IPR_9.2_1 -DZ=15 PR_9.2_1/Lab_09_2_1.cpp -o $@

Lab_09_2_1_b2: PR_9.2_1/Lab_09_2_1.cpp PR_9.2_1/macros.h
	$(CXX) $(CXXFLAGS) -IPR_9.2_1 -DZ=5 PR_9.2_1/Lab_09_2_1.cpp -o $@

tests: $(TESTS)

tests/UnitTest_09_1: tests/UnitTest_09_1.cpp PR_9.1/var.cpp PR_9.1/dod.cpp PR_9.1/sum.cpp PR_9.1/var.h PR_9.1/dod.h PR_9.1/sum.h tests/doctest.h
	$(CXX) $(CXXFLAGS) -IPR_9.1 -Itests PR_9.1/var.cpp PR_9.1/dod.cpp PR_9.1/sum.cpp tests/UnitTest_09_1.cpp -o $@

tests/UnitTest_09_2_1: tests/UnitTest_09_2_1.cpp PR_9.2_1/macros.h tests/doctest.h
	$(CXX) $(CXXFLAGS) -IPR_9.2_1 -Itests tests/UnitTest_09_2_1.cpp -o $@

test: check
check: tests
	@echo "=================================================="
	@echo "Running all Unit Tests..."
	@echo "=================================================="
	@./tests/UnitTest_09_1
	@./tests/UnitTest_09_2_1
	@echo "=================================================="
	@echo "ALL TESTS PASSED SUCCESSFULLY!"
	@echo "=================================================="

clean:
	rm -rf $(PROGRAMS) $(TESTS) *.dSYM tests/*.dSYM PR_9.1/*.dSYM PR_9.2_1/*.dSYM
