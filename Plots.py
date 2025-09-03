import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def main():
    # Mappen der filene ligger
    folder = "NO1_FCR_Volumes"   # <-- bytt til riktig sti

    # Finn alle csv-filer som matcher mønsteret
    files = glob.glob(os.path.join(folder, "GUI_BALANCING_OFFERS_AND_RESERVES_*.csv"))
    files.sort()  # sorterer etter filnavn (årstall i stigende rekkefølge)

    # Les alle filer og samle i én DataFrame
    df_list = []
    for f in files:
        print(f"Laster {f}")
        temp = pd.read_csv(f)
        temp['ISP (CET/CEST)'] = pd.to_datetime(temp['ISP (CET/CEST)'], errors='coerce')
        df_list.append(temp)

    df = pd.concat(df_list, ignore_index=True)

    # Sjekk tidsperiode
    print("Tidsperiode:", df['ISP (CET/CEST)'].min(), "→", df['ISP (CET/CEST)'].max())

    # Kolonner vi vil se på
    cols_to_plot = [
        'Regulation Up - Accepted [17.1.D] (MW)',
        'Regulation Up - Activated [17.1.E] (MWh)',
        'Regulation Down - Accepted [17.1.D] (MW)',
        'Regulation Down - Activated [17.1.E] (MWh)'
    ]

    # Sorter etter tid
    df = df.sort_values(by='ISP (CET/CEST)')

    # Lag et samlet plott med fire subplots
    fig, axes = plt.subplots(len(cols_to_plot), 1, figsize=(14,10), sharex=True)

    for ax, col in zip(axes, cols_to_plot):
        ax.plot(df['ISP (CET/CEST)'], df[col], linewidth=0.7)
        ax.set_title(col)
        ax.set_ylabel(col.split('[')[0].strip())
        ax.grid(True)

    plt.xlabel("Tid")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
