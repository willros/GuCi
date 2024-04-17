import pyfastx
import polars as pl
import matplotlib.pyplot as plt
import warnings
import argparse
from pathlib import Path

warnings.filterwarnings("ignore")


def fastx_file_to_df(fastx_file: str) -> pl.DataFrame:
    fastx = pyfastx.Fastx(fastx_file)
    reads = list(zip(*[[x[0], x[1]] for x in fastx]))

    df = (
        pl.DataFrame(
            {
                "name": reads[0],
                "sequence": reads[1],
            }
        )
        .select(pl.col("sequence").str.split("").explode(), pl.col("name"))
        .filter(pl.col("sequence") != "")
        .with_row_index(name="position", offset=1)
    )

    return df


def add_gc(df) -> pl.DataFrame:
    return df.with_columns(
        gc=pl.when(pl.col("sequence").str.contains("G|C")).then(1).otherwise(0)
    )


def add_rolling_mean(df, window):
    return df.with_columns(rolling_gc=pl.col("gc").rolling_mean(window_size=window))


def plot_gc(df, title):
    fig = plt.figure(figsize=(50, 15))
    plt.plot(df["position"], df["rolling_gc"])
    plt.gca().set_yticklabels([f"{x:.0%}" for x in plt.gca().get_yticks()])
    plt.gca().xaxis.set_major_formatter(
        plt.matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
    )
    plt.ylabel("% GC content")
    plt.xlabel("Position")
    plt.title(title)
    plt.close()
    return fig


def make_dir(outpath: str) -> None:
    outpath = Path(outpath)
    if not outpath.exists():
        outpath.mkdir(parents=True)


def cli():
    parser = argparse.ArgumentParser(description="GC content")
    parser.add_argument("-f", "--fasta", required=True, help="Fasta file")
    parser.add_argument(
        "-w",
        "--window",
        required=True,
        type=int,
        help="Size of sliding window",
    )
    parser.add_argument(
        "-o",
        "--out_folder",
        required=False,
        default=".",
        help="Output folder",
    )

    args = parser.parse_args()

    main(
        fasta=args.fasta,
        window=args.window,
        out_folder=args.out_folder
    )


def main(fasta, window, out_folder):

    df = fastx_file_to_df(fasta)
    df = add_gc(df)
    df = add_rolling_mean(df, window)

    title = f"GC content of: {Path(fasta).stem}. Rolling window: {window}"
    plot = plot_gc(df, title)

    make_dir(out_folder)
    out_name = f"{out_folder}/gc_{Path(fasta).stem}.pdf"
    plot.savefig(out_name)


if __name__ == "__main__":
    cli()
    exit(0)
