# Implement Autocomplete and Full Text Search with Elastic Search

## Index

- [Autocomplete](#autocomplete)
- [Full Text Search](#full-text-search)
- [Implementation](#implementation)
- [Development Environment](#development-environment)
- [Reference](#reference)

## Autocomplete

### About Autocomplete

- Autocomplete, or word completion, is a feature in which an application predicts the rest of a word a user is typing.
- It is also known as Search as you type or Type Ahead Search. It helps in navigating or guiding a user by prompting them with likely completions and alternatives to the text as they are typing it. It reduces the amount of characters a user needs to type before executing any search actions, thereby enhancing the search experience of users.
- Elasticsearch is used to implement autocomplete.

### Approaches

1. **Search as You Type** (ngram/token-based approach)

   **Use Case**: Search as you type is typically employed when providing real-time, partial matching autocomplete suggestions as users interact with a search box. It's commonly utilized for auto-suggest functionality in search applications.

   **Implementation**: This method involves creating custom analyzers using ngram or edge ngram tokenizers and filters to generate partial word or character-based tokens. These tokens are then indexed and queried to offer autocomplete suggestions.

   **Advantages**:

   - Offers real-time suggestions as users type.
   - Customizable to suit specific requirements.
   - Applicable to a broad range of use cases beyond autocomplete, including partial word matching.

   **Disadvantages**:

   - Requires careful configuration and tuning to prevent performance and storage issues, particularly with large datasets.
   - Not suitable for searching entire phrases.

2. **Completion Suggester**

   **Use Case**: The completion field type is purpose-built for autocomplete scenarios where suggestions are based on pre-defined phrases or terms. It's optimized for rapid and efficient autocompletion.

   **Implementation**: To implement this, you create a dedicated "completion" field within your Elasticsearch mapping. This field is designed to store a list of terms or phrases to suggest in autocomplete. Elasticsearch employs a data structure known as a finite state transducer (FST) to efficiently retrieve suggestions.

   **Advantages**:

   - Offers extremely fast and efficient autocomplete functionality, ideal for large datasets.
   - Supports phrase matching and can provide complete suggestions.

   **Disadvantages**:

   - Not suitable for partial word matching or wildcard searches.
   - Requires pre-defined terms or phrases to be stored in the index.

   3. **Summary**

   - Opt for "Search as You Type" when real-time, partial matching autocomplete suggestions are required, along with flexibility in matching criteria.
   - Choose the "Completion field type" when seeking highly efficient autocomplete functionality with pre-defined terms or phrases, without the need for partial word matching.

## Full Text Search

### Benefits of Full-Text Search in Elasticsearch

- **Flexibility**: Full-text search allows you to search for documents based on a variety of criteria, including keywords, phrases, synonyms, and even misspellings.

- **Relevance**: Elasticsearch uses a variety of techniques to rank search results based on relevance, ensuring that the most relevant documents are returned first.

- **Scalability**: Elasticsearch is a scalable search engine, making it ideal for handling large volumes of data.

### Types of Full-Text Search in Elasticsearch

- **Multi-match search**: This type of search allows you to search for documents that contain a match for your query string in one or more fields.

- **Phrase search**: This type of search looks for documents that contain an exact match for your query phrase, including the order of the words.

### Implementation

1. **Define the Scoring Script:**

   The `define_template_search` function defines a scoring script that calculates a score for each document based on three factors:

   - `sale_rate_score`: A score based on the sale rate of the item.
   - `sales_number_score`: A score based on the number of sales the item has had.
   - `sale_item_price_score`: A score based on the price of the item.

   The script is written in Mustache and is designed to be flexible and adaptable to different scoring requirements.

2. **Create the Multi-Match Query:**

   The template uses a multi-match query to search for items that match the specified query string. The query searches two fields: `item_name` and `shop_name`.

3. **Add Fuzzy Matching:**

   To improve search relevance, the template includes a fuzzy matching query that allows for typos and misspellings. The fuzziness level is set to "AUTO," which automatically adjusts the fuzziness based on the length of the query string.

4. **Combine Queries and Scoring:**

   The template combines the multi-match query and the scoring script using a `function_score` query. This allows the search results to be ranked based on both relevance and the calculated score.

5. **Create and Save the Template:**

The `put_script` API is used to create and save the search template in Elasticsearch.

### Usage Example

    ```json
    {
    "size": 20,
    "query": {
        "template": {
        "id": "fuzzy-search",
        "params": {
            "query_string": "My query string"
        }
        }
    }
    }
    ```

This query would return the top 20 documents that match the query string, ranked based on relevance and the calculated score.

## Development Environment

1. **Create Environment and Install Packages**

   ```shell
   conda create -n text-search python=3.9
   ```

   ```shell
   conda activate text-search
   ```

   ```shell
   pip install -r requirements.txt
   ```

2. **Run the Application**

   ```shell
   uvicorn app:app --port 7000
   ```

## Reference

- [Elasticsearch Autocomplete Functionality](https://taranjeet.medium.com/elasticsearch-building-autocomplete-functionality-494fcf81a7cf)
- [Elasticsearch Image Search Example](https://www.sbert.net/examples/applications/image-search/README.html)
- [Elasticsearch Search Suggesters](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html#completion-suggester)
