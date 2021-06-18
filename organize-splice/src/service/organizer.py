import argparse
import os
import shutil
import sys

_organized_dir_ = "_organizer_processed"

class Organizer:
    def __init__(self, splice_directory, destination, move):
        self.organizer_processed_dir = _organized_dir_
        self.splice_directory = splice_directory
        self.destination = destination
        self.top_levels = {
            '808s': ['808', 'bass'],
            'kicks': ['kick'],
            'hihats': ['hihat', 'hh', 'hi_hat', 'open_hat', 'hat'],
            'claps': ['clap'],
            'snares': ['snare'],
            'percs': ['rim'],
            'pads': ['pad'],
            'plucks': ['pluck'],
            'keys': ['key', 'piano'],
            'bells': ['bell'],
            'guitar': ['guitar'],
            'fx': ['fx'],
            'vocals': ['vocal'],
            'loops': ['loop'],
            'one_shots': ['one_shot']
        }
        self.move = move
        if self.move:
            if not os.path.exists(self.organizer_processed_dir):
                os.makedirs(self.organizer_processed_dir)
        self.processed_directory = os.path.join(self.splice_directory, self.organizer_processed_dir)
        print(self.processed_directory)

    def organize(self):
        # print("organizing... %s to %s" % (self.splice_directory, self.destination))
        for subdir, dirs, files in os.walk(self.splice_directory):
            for file in files:
                copy_decided = False
                if not file.endswith('.asd') or not file.endswith('.txt'):
                    sample = os.path.join(subdir, file)

                    for k, v in self.top_levels.items():
                        for option in v:
                            # print(option, sample)
                            if option.lower() in file.lower() or option.lower() in sample.lower():
                                copy_decided = True
                                # print('directory chosen: %s' % k)
                                end_destination = os.path.join(self.destination, k)
                                if not os.path.exists(end_destination):
                                    os.makedirs(end_destination)

                                dest = os.path.join(end_destination, file)
                                # print("Copying: %s\nTo: %s" % (sample, dest))
                                try:
                                    shutil.copyfile(sample, dest)
                                except:
                                    print("Copy Error: %s" % sample)
                                    print("Unexpected error:", sys.exc_info()[0])
                                    copy_decided = True

                                if self.move:
                                    shutil.move(sample, self.processed_directory)
                                break
                        if copy_decided:
                            break
                    if not copy_decided:
                        # print(k, v, sample)
                        # when file placement can't be determined
                        end_destination = os.path.join(self.destination, 'misc')
                        if not os.path.exists(end_destination):
                            os.makedirs(end_destination)

                        dest = os.path.join(end_destination, file)
                        shutil.copyfile(sample, dest)
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="organize damn splice")
    parser.add_argument(
        "--splice-folder",
        help='location of splice samples'
    )
    parser.add_argument(
        "--destination",
        help='location of organized files'
    )
    parser.add_argument(
        "--move",
        type=bool,
        default=False,
        help="move files to processed folder, creates \"" + _organized_dir_ + "\" folder within Splice's \"Sample\" directory"
    )

    args = parser.parse_args()

    o = Organizer(args.splice_folder, args.destination, args.move)
    o.organize()
