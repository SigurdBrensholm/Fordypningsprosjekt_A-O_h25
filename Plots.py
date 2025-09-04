import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def main():
    # Mappen der filene ligger
    folder = "Fordypningsprosjekt_A-O_h25/NO1_FCR_Volumes"

    # Finn alle csv-filer som matcher mønsteret
    files = glob.glob(os.path.join(folder, "GUI_BALANCING_OFFERS_AND_RESERVES_*.csv"))
    files.sort()  # sorterer etter filnavn (årstall i stigende rekkefølge)

    # Les alle filer og samle i én DataFrame
    df_list = []
    for f in files:
        print(f"Laster {f}")
        temp = pd.read_csv(f)
        # Ekstraher starttidspunktet fra intervallet før konvertering
        temp['ISP (CET/CEST)'] = temp['ISP (CET/CEST)'].astype(str).str.split(' - ').str[0]
        temp['ISP (CET/CEST)'] = pd.to_datetime(temp['ISP (CET/CEST)'], dayfirst=True, errors='coerce')
        df_list.append(temp)

    df = pd.concat(df_list, ignore_index=True)
    print(df)

    # Sjekk tidsperiode
    print("Tidsperiode:", df['ISP (CET/CEST)'].min(), "→", df['ISP (CET/CEST)'].max())

    # Kolonner vi vil se på
    cols_to_plot = [
        'Regulation Up - Accepted [17.1.D] (MW)',
        'Regulation Up - Activated [17.1.E] (MWh)',
        'Regulation Down - Accepted [17.1.D] (MW)',
        'Regulation Down - Activated [17.1.E] (MWh)'
    ]

    # Konverter 'n/e' til NaN og fyll NaN med 0 i kolonnene som skal plottes
    for col in cols_to_plot:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df[cols_to_plot] = df[cols_to_plot].fillna(0)
    print(df)
    # Debug: Skriv ut antall rader og noen eksempler
    print(f"Antall rader etter utfylling: {len(df)}")
    print("Eksempel på tidspunkter:", df['ISP (CET/CEST)'].head())
    for col in cols_to_plot:
        print(f"Eksempel på {col}: ", df[col].head())

    # Aggreger til månedlige summer
    df['month'] = df['ISP (CET/CEST)'].dt.to_period('M')
    monthly = df.groupby('month')[cols_to_plot].sum().reset_index()
    monthly['month'] = monthly['month'].dt.to_timestamp()

    # Plott MW-kolonner sammen og MWh-kolonner sammen, med tydelig tittel
    mw_cols = [col for col in cols_to_plot if '(MW)' in col]
    mwh_cols = [col for col in cols_to_plot if '(MWh)' in col]

    # MW-plott
    plt.figure(figsize=(14,5))
    for col in mw_cols:
        plt.plot(monthly['month'], monthly[col], marker='o', linewidth=1.2, label=col)
    plt.title('FCR-NO1 – Månedlig MW-volum')
    plt.ylabel('MW')
    plt.xlabel('Måned')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # MWh-plott
    plt.figure(figsize=(14,5))
    for col in mwh_cols:
        plt.plot(monthly['month'], monthly[col], marker='o', linewidth=1.2, label=col)
    plt.title('FCR-NO1 – Månedlig MWh-volum')
    plt.ylabel('MWh')
    plt.xlabel('Måned')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
