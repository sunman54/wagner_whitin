import pandas as pd

def wagner_within(talepler, stok_maliyeti, uretim_maliyeti):
    n = len(talepler)
    
    # dp tablosu, en küçük toplam maliyeti içerir
    dp = [float('inf')] * (n + 1)
    
    # Her dönemde ne kadar üretim yapılacağını ve dönemlik maliyetleri saklamak için liste
    uretim_planlari = [[] for _ in range(n + 1)]
    dönemlik_maliyetler = [[] for _ in range(n + 1)]
    
    # Temel durum: 0. periyottaki maliyet = 0
    dp[0] = 0
    
    for i in range(1, n + 1):
        for j in range(i):
            # Üretim miktarını belirle
            uretim_miktari = sum(talepler[j:i])
            
            # Toplam maliyeti güncelle
            toplam_maliyet = dp[j] + stok_maliyeti * (i - j) + uretim_maliyeti * uretim_miktari
            
            if toplam_maliyet < dp[i]:
                dp[i] = toplam_maliyet
                # Üretim planını ve dönemlik maliyeti güncelle
                uretim_planlari[i] = uretim_planlari[j] + [uretim_miktari]
                dönemlik_maliyetler[i] = dönemlik_maliyetler[j] + [uretim_miktari * uretim_maliyeti]

    return dp[n], uretim_planlari, dönemlik_maliyetler

# Örnek kullanım
talepler = [50, 60, 90, 70, 30, 100, 60, 40, 80 ,20]
stok_maliyeti = 1
uretim_maliyeti = 300

toplam_maliyet, uretim_planlari, dönemlik_maliyetler = wagner_within(talepler, stok_maliyeti, uretim_maliyeti)

# Sonuçları DataFrame'e dönüştürme
df = pd.DataFrame({
    'Dönem': range(1, len(uretim_planlari)),
    'Üretim Miktarı': [sum(plan) for plan in uretim_planlari[1:]],
    'Dönemlik Maliyet': [sum(maliyet) for maliyet in dönemlik_maliyetler[1:]]
})

print("Optimal Toplam Maliyet:", toplam_maliyet)
print(df)
