import stockdaq.data.alpha_vantage_downloader as av_downloader
import stockdaq.data.yfinance_downloader

downloader_dict = {
    "Alpha Vantage": av_downloader.AlphaVantageDownloader,
    "yfinance": stockdaq.data.yfinance_downloader.yfinanceDownloader,
}
