import subprocess
import threading
import os, sys


class ProgressTracker:
    """Class to track and display progress."""

    def __init__(self, total_tests):
        self.total_tests = total_tests
        self.completed_tests = 0

    def update(self):
        self.completed_tests += 1
        display_progress(self.total_tests, self.completed_tests)


def run_test(test_name, progress_tracker):
    output_file = "../test/test-outputs/" + test_name + "out.log"
    cmd = ["ctest", "-R", "InputAndRun_" + test_name, "--output-on-failure", "-V"]
    with open(output_file, "w") as f:
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Write stdout and stderr to the file
        for line in process.stdout:
            f.write(line)
        for line in process.stderr:
            f.write(line)

        process.wait()
    progress_tracker.update()


def inital_test():
    os.chdir("../test")
    os.system("./check-cards.sh")


def final_test():
    cmd = ["ctest", "-R", "Finalize", "-V"]
    subprocess.Popen(cmd)
    subprocess.Popen(["rm", "-r", "../test/ci-setups"])


def display_progress(total_tests, completed_tests):
    percentage = (completed_tests / total_tests) * 100
    sys.stdout.write(
        f"\rProgress: {percentage:.2f}% ({completed_tests}/{total_tests} tests completed)"
    )
    sys.stdout.flush()


def main():
    inital_test()
    # Change to the directory where tests should be run
    build_dir = "../build"
    os.chdir(build_dir)

    test_names = ["Sherpa", "KKMC", "Madgraph", "Babayaga", "Pythia"]
    progress_tracker = ProgressTracker(total_tests=len(test_names))
    display_progress(len(test_names), 0)

    # Create a thread for each test
    threads = []
    for test in test_names:
        thread = threading.Thread(target=run_test, args=(test, progress_tracker))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    final_test()
    display_progress(len(test_names), len(test_names))
    print("\nAll tests have been executed. Check the output files for details.")


if __name__ == "__main__":
    main()
