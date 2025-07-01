# Finance News Summarizer (Streamlit + Docker)

📄️ An application for summarizing financial news using T5-small + LoRA.

---

## 📦 Quick Start with Docker

🗕️ Make sure you have a recent version of Docker and `docker compose` installed.

1. Clone the repository:

   ```bash
   git clone https://github.com/DCel567/finance_summary_app
   cd finance_rag
   ```

2. Start the container:

   ```bash
   docker compose up
   ```

   On first run, the Docker image will be built automatically.\
   Then the app will be available at:\
   📍 [**http://localhost:8501**](http://localhost:8501)

3. If you made changes (e.g., updated code or dependencies), restart with rebuild:

   ```bash
   docker compose up --build
   ```

---

## 🚧 Running Without Docker

If you'd prefer to run locally:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app_feed.py
```

---

## 🗂️ Project Structure

```
finance_rag/
├── app_feed.py            # Streamlit app (news feed)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image build instructions
├── docker-compose.yml     # Simplified startup with Docker Compose
├── train.ipynb            # Training script
├── eval.ipynb             # Evaluation script
├── data/                  # Data files
└── LORA/                  # Folder with fine-tuned LoRA models
   ├── t5_small_1/
   └── ...
```

---

## Features

- **AI-powered summarization** using T5 models (base or fine-tuned)
- **Financial news feed** from Financial Modeling Prep API
- **Customizable filters**:
  - Portfolio tickers (e.g., AAPL, GOOGL)
  - Keywords/phrases (e.g., "Elon Musk", "AI")
  - Default company/keyword suggestions
- **Interactive UI** with:
  - Manual article input
  - API news fetching
  - Expandable original articles
- **Model options**:
  - Base fine-tuned T5-small model
  - Optional original T5-small model

---

## 🧠 Summarization Model Toggle

- **[✓] Use fine-tuned model** — when checked and the folder `t5-lora-summarizer` is present, your LoRA fine-tuned model will be used.
- Otherwise, the base model `t5-small` is used.

---

### Basic Workflow

1. **Select model type** (base or fine-tuned)
2. **Set filters**:
   - Enter portfolio tickers (comma/space separated)
   - Add custom keywords
   - Select from default keywords
3. Choose input method:
   - **Manual input**: Paste/write article text
   - **API fetch**: Get latest financial news matching your filters
4. View summarized articles in the feed
5. Expand any article to see the original text

## Configuration

Key settings in the code:
- `BASE_MODEL_NAME`: "t5-small" (base model)
- `FINETUNED_MODEL_PATH`: "LORA/t5_small_2" (fine-tuned model)
- `DEVICE`: Automatically uses CUDA if available
- `DEFAULT_KEYWORDS`: Predefined list of common financial keywords

## API Integration

The app uses Financial Modeling Prep's API for news articles:
- Endpoint: `https://financialmodelingprep.com/api/v3/fmp/articles`
- Requires API key (provided in code)

## Models

1. **Base Model**: Standard T5-small from HuggingFace
2. **Fine-tuned Model**: LoRA-adapted T5-small for summarization
   - [BBC Articles Dataset with Extra Features](https://www.kaggle.com/datasets/jacopoferretti/bbc-articles-dataset)
   - Parsed and summarized with [Pegasus](https://huggingface.co/human-centered-summarization/financial-summarization-pegasus) [FMP](https://financialmodelingprep.com) articles

## Model Fine-tuning

1. **rouge1**: 0.22
2. **rouge2**: 0.13
3. **rougeL**: 0.20
4. **rougeLsum**: 0.20
5. **bert_score precision**: 0.8729
6. **bert_score recall**: 0.8508
7. **bert_score f1**: 0.8508

## Known Limitations

- API rate limits may apply when fetching news
- Summarization quality depends on model capabilities
- Fine-tuned model path is hardcoded


## 🚀 Possible Improvements

- Automatic news refresh every N minutes
- Improved portfolio management
- Improved hallucination detection
- Summarization confidence scores
- Api key protection

## Example Output

### Text 1
```text
JPMorgan reiterated its Underweight rating and $115 price target on Tesla (NASDAQ:TSLA), citing signs of continued weak demand and forecasting a sharper year-over-year decline in Q2 deliveries than previously expected. The firm now estimates Tesla will deliver just 360,000 vehicles in the second quarter, down 19% year-over-year compared to 444,000 deliveries a year ago and representing an 8% shortfall versus consensus of 392,000. JPMorgan’s new forecast is also 6.5% below Tesla’s own compiled consensus of 385,000. The updated view reflects analysis of May sales trends in key markets with reliable data—such as Europe—alongside third-party estimates for other regions like the U.S., plus insurance registration data for China through late June. JPMorgan’s revised Q2 delivery forecast represents a 9% cut from its prior estimate of 395,000 made in April. The lowered expectations underscore JPMorgan’s concerns about persistent demand softness for Tesla vehicles, which it believes could weigh further on volumes and financial performance, reinforcing its cautious stance on the stock.
```
### Summary 1
```text
JPMorgan reiterated its Underweight rating and $115 price target on Tesla (NASDAQ:TSLA). The firm now estimates Tesla will deliver just 360,000 vehicles in the second quarter, down 19% year-over-year compared to 444,000 deliveries a year ago.
```

### Text 2
```text
Prices for China‑made goods on Amazon have climbed 2.6% from January through mid‑June—faster than overall core goods inflation. Here’s a concise, mobile‑friendly breakdown of what’s happening, who’s feeling the squeeze, and how to stay ahead with Financial Modeling Prep’s APIs. 1. Tariff Pass‑Through Is Here Tariffs imposed on Chinese imports began in May to protect U.S. manufacturers—but now consumers are seeing the impact. DataWeave Analysis:Reviewed 1,407 China‑origin products on Amazon.Median basket price up 2.6% vs. 1% increase in core goods CPI. Third‑Party Sellers:Account for 62% of those items—many are smaller merchants with less margin buffer. 2. Inflation vs. E‑Commerce Pricing Consumers assume e‑retail discounts beat brick‑and‑mortar, but rising input costs and shipping fees are eroding those savings. Core Goods CPI:Federal data shows a 1% rise over six months (annualized 2%). Amazon Basket:Outpacing that, signaling direct tariff pass‑through. Tip: Automate CPI tracking by scheduling alerts with the Economics Calendar API. 3. Commodity Costs & Supply‑Chain Pressures Input prices for steel, aluminum and plastics feed into consumer‑goods costs. Metal & Energy Inputs:Use the Commodities API to monitor raw‐material trends that often foreshadow retail price shifts. 4. What It Means for Consumers and Retailers Consumers:Look for product substitutes or earlier holiday deals to lock in current prices. Retailers:Must decide whether to absorb tariffs or pass costs on—analyzing real‑time commodity and CPI data can guide that choice. ConclusionTariffs are no longer a distant policy debate—they’re directly inflating the prices of everyday Amazon purchases. Call‑to‑ActionUse Financial Modeling Prep’s APIs to automate CPI and commodity tracking—and turn data into pricing strategy.
```
### Summary 2
```text
Core Goods CPI:Federal data shows a 1% rise over six months (annualized 2%). Metal & Energy Inputs:Use the Commodities API to monitor rawmaterial trends that often foreshadow retail price shifts. ConclusionTariffs are no longer a distant policy debate—they’re directly inflating the prices of everyday Amazon purchases.
```