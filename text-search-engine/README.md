# Implement Autocomplete and Full-text Search with Elastic Search
## Autocomplete 
### About autocomplete
- Autocomplete, or word completion, is a feature in which an application predicts the rest of a word a user is typing
- It is also known as Search as you type or Type Ahead Search. It helps in navigating or guiding a user by prompting them with likely completions and alternatives to the text as they are typing it. It reduces the amount of character a user needs to type before executing any search actions, thereby enhancing the search experience of users.
- Elasticsearch is used to implement autocomplete.
### Approaches
There are several approaches available for building autocomplete functionality in Elasticsearch. We will explore the following three methods:

#### Prefix Query
The Prefix Query approach involves utilizing a prefix query against a custom field. Terms are stored as keywords, allowing multiple words to be stored together as a single term. However, this approach has limitations such as matching only at the term's beginning and potential performance issues for large datasets.

#### Edge Ngram
The Edge Ngram approach employs different analyzers during indexing and searching. During indexing, a custom analyzer with an edge n-gram filter is used to break text into fragments. At search time, a standard analyzer prevents query splitting. This method allows effective mid-text query matches, but it might lead to slower indexing and storage for larger indices.

#### Completion Suggester
Elasticsearch offers an in-house solution called the Completion Suggester. It utilizes a Finite State Transducer (FST) for in-memory data storage. FST is stored per segment, enabling horizontal scalability as new nodes are added. When implementing this approach, consider factors such as completion types for autosuggest items, handling various names for a single term, and assigning weights to documents for ranking control.

## Refrence
https://taranjeet.medium.com/elasticsearch-building-autocomplete-functionality-494fcf81a7cf

Three types of suggesters:
- Completion
- Term
- Phrase

### Completion suggester
- Provide autocomplete
- Only works based on prefix
- Stored as special data structure for speed
    - Costly to build
    - Stored in memory
    

uvicorn app:app


## Search as You Type (ngram/token-based approach):

**Use Case**: Search as you type is typically employed when providing real-time, partial matching autocomplete suggestions as users interact with a search box. It's commonly utilized for auto-suggest functionality in search applications.

**Implementation**: This method involves creating custom analyzers using ngram or edge ngram tokenizers and filters to generate partial word or character-based tokens. These tokens are then indexed and queried to offer autocomplete suggestions.

**Advantages**:
- Offers real-time suggestions as users type.
- Customizable to suit specific requirements.
- Applicable to a broad range of use cases beyond autocomplete, including partial word matching.

**Disadvantages**:
- Requires careful configuration and tuning to prevent performance and storage issues, particularly with large datasets.
- Not suitable for searching entire phrases.

## Completion Field Type:

**Use Case**: The completion field type is purpose-built for autocomplete scenarios where suggestions are based on pre-defined phrases or terms. It's optimized for rapid and efficient autocompletion.

**Implementation**: To implement this, you create a dedicated "completion" field within your Elasticsearch mapping. This field is designed to store a list of terms or phrases to suggest in autocomplete. Elasticsearch employs a data structure known as a finite state transducer (FST) to efficiently retrieve suggestions.

**Advantages**:
- Offers extremely fast and efficient autocomplete functionality, ideal for large datasets.
- Supports phrase matching and can provide complete suggestions.

**Disadvantages**:
- Not suitable for partial word matching or wildcard searches.
- Requires pre-defined terms or phrases to be stored in the index.

### In summary:
- Opt for "Search as You Type" when real-time, partial matching autocomplete suggestions are required, along with flexibility in matching criteria.
- Choose the "Completion field type" when seeking highly efficient autocomplete functionality with pre-defined terms or phrases, without the need for partial word matching.


### How to rank
- Top sale number
- Sale rate
- Low fixed price

### Refrence
https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html#completion-suggester