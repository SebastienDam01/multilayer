import argparse

def _get_parser():
    """Parse command line inputs for this function.

    Returns
    -------
    parser.parse_args() : argparse dict
    """
    parser = argparse.ArgumentParser(
        description=(
            "Multilayer, a toolbox for multilayer network analyses "
            "It uses a supra-adjacency matrix "
            "(generated in MATLAB) as input, "
            "and creates a multilayer network "
            "object - similar to the ones in Networkx. "
            "For privacy reasons, we provide a random MST file. \n"
        ),
        add_help=False,
    )
    opt_in = parser.add_argument_group("Optional Arguments for Input")
    opt_in.add_argument(
        "-fname",
        "--input-func",
        dest="filename",
        type=str,
        help=(
            "Filename of the input data. "
            "Default is supra_randmst.mat"
        ),
        default="supra_randmst.mat",
    )
    
    opt_params = parser.add_argument_group("Optional Arguments for Layer Parametrization")
    opt_params.add_argument(
        "-l",
        "--input-layer",
        dest="layer_number",
        type=bool,
        help=(
            "Specify the number of layer. "
            "Default is 8."
        ),
        default=8,
    )
    opt_params.add_argument(
        "-s",
        "--input-size",
        dest="layer_size",
        type=int,
        help=(
            "Specify the number of regions/nodes per layer. "
            "Default is 210."
        ),
        default=210,
    )
    opt_params.add_argument(
        "-w",
        "--weighting",
        dest="weight",
        type=bool,
        help=(
            "Specify whether data is weighted or unweighted. "
            "Default is False."
        ),
        default=False,
    )

    optional = parser.add_argument_group("Other Optional Arguments")

    optional.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit"
    )
    optional.add_argument(
        "-f",
        "--function-multilayer",
        dest="function",
        type=str,
        help=(
            "Multilayer function for the "
            "calculation of multilayer network metrics. "
            "Default is group_eigenvector_centrality"
        ),
        default="get_multi_eigenvector_centrality",
    )

    return parser


if __name__ == "__main__":
    print("Running MULTINET Multilayer.")