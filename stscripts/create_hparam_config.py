#! /u/bulk/home/wima/fchrstou/workspace/RL_RSA_MDPs/exp2/venv_rlrsamdp/bin/python
# print("Running")
import tensorflow as tf
from tensorboard.plugins.hparams import api as hp
import os
import sys
import toml

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "5"


METRIC_avgrew = "avg_reward"
METRIC_eps = "eps"
METRIC_EvalRew = "eval_reward"
METRIC_EvalSteps = "eval_steps"
METRIC_loss = "loss"
METRIC_grad = "grad_val"

# METRIC_avgrew = "Epsisode Statistics/avg_reward"
# METRIC_eps = "Epsisode Statistics/eps"
# METRIC_EvalRew = "Epsisode Statistics/eval_reward"
# METRIC_EvalSteps = "Epsisode Statistics/eval_steps"
# METRIC_loss = "Epsisode Statistics/loss"
# METRIC_grad = "Epsisode Statistics/grad_val"
# Julia parsed paramsdict
stpd = toml.load("UserTemp/simtreeparams.toml")
print(stpd)
hparamsconfig = [hp.HParam(par, hp.Discrete(stpd[par])) for par in stpd]


def write_config(path):
    with tf.summary.create_file_writer(path).as_default():
        # with tf.summary.create_file_writer("log").as_default():
        hp.hparams_config(
            hparams=hparamsconfig,
            metrics=[
                hp.Metric(METRIC_avgrew, display_name="avgrew"),
                hp.Metric(METRIC_eps, display_name="episodes"),
                hp.Metric(METRIC_EvalRew, display_name="evalrew"),
                hp.Metric(METRIC_EvalSteps, display_name="evalsteps"),
                hp.Metric(METRIC_loss, display_name="loss"),
                hp.Metric(METRIC_grad, display_name="grad"),
                # hp.Metric(, display_name="Accuracy"),
                # hp.Metric(, display_name="Accuracy"),
            ],
        )


def print_usage():
    print("Usage: python script.py <path>")
    print("Options:")
    print("  -h, --help: Show this help message")


if __name__ == "__main__":
    # Check if the command-line argument for the path is provided
    if len(sys.argv) == 1:
        print_usage()
        sys.exit(1)  # Exit with error status

    # Check if the help flag is provided
    if sys.argv[1] in ("-h", "--help"):
        print_usage()
        sys.exit(0)  # Exit without error status

    # Extract the path from command-line arguments
    if len(sys.argv) != 2:
        print("Error: Only one argument (path) allowed.")
        print_usage()
        sys.exit(1)  # Exit with error status
    path = sys.argv[1]

    # Call the function with the provided path
    write_config(path)
# Make main function with Keywoard argument for path
# on study modify run sh to put study root / Results
