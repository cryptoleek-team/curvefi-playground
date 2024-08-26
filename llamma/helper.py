import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

def display_erc20(balance, decimals=18):
    return f"{balance / 10 ** decimals:,.3f}"

# Helper Functions
def user_balances(user_addr, crvusd, collateral, decimals=18, user_name="User"):
    print(f"{user_name} Balances:")
    print(f" - crvUSD: {crvusd.balanceOf(user_addr) / 10 ** 18:,.4f}")
    print(f" - {collateral.symbol()}: {collateral.balanceOf(user_addr) / 10 ** decimals:,.4f}")


def plot(amm, user):
    bands = range(
        min(0, amm.active_band(), amm.read_user_tick_numbers(user)[0]),
        max(amm.active_band(), amm.read_user_tick_numbers(user)[1]) + 1,
    )

    p_min = [amm.p_oracle_down(n) for n in bands]
    p_max = [amm.p_oracle_up(n) for n in bands]
    y_values = [amm.bands_y(n) for n in bands]

    fig, ax = plt.subplots(figsize=(16, 8))  # Increased figure width
    grey_cmap = plt.colormaps["Greys"]

    for i, (min_val, max_val, y_val) in enumerate(zip(p_min, p_max, y_values)):
        width = max_val - min_val

        if bands[i] == amm.active_band():
            color = "green"
            edge_color = "darkgreen"
            text_color = "darkgreen"
        else:
            color = grey_cmap(0.3 + (i / len(bands)) * 0.5)
            edge_color = grey_cmap(0.5 + (i / len(bands)) * 0.5)
            text_color = "black"

        rect = plt.Rectangle(
            (min_val, 0),
            width,
            y_val,
            fill=True,
            facecolor=color,
            alpha=0.3,
            edgecolor=edge_color,
            linewidth=2,
        )
        ax.add_patch(rect)

        ax.plot([min_val, max_val], [y_val, y_val], color=edge_color, linewidth=2)

        ax.text(
            (min_val + max_val) / 2,
            -max(y_values) * 0.05,
            f"Band {bands[i]}",
            ha="center",
            va="top",
            color=text_color,
            rotation=45,  # Rotate labels
            fontsize=8,  # Reduce font size
        )

    ax.set_xlabel("Price (p)")
    ax.set_ylabel("Collateral")
    ax.set_title(f"Price Range and Collateral for User {user}")

    ax.set_xscale('log')  # Set x-axis to logarithmic scale
    ax.set_ylim(bottom=-max(y_values) * 0.1)

    # Format x-axis labels with more precision
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.6e}"))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()