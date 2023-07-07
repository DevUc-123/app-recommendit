

import streamlit as st
import pickle
import numpy as np

st.header('Book Recommendation System')

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

book_list = pt.index.tolist()
selected_book = st.selectbox("Type or select a book from the dropdown", book_list)

if st.button('Show Book Recommendation', key='recommendation_button'):
    if selected_book in pt.index:
        index = np.where(pt.index == selected_book)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)

        cols = st.columns(4)  # Adjust the number of columns as per your preference

        # Display the selected book at the top
        selected_book_title = pt.index[index]
        selected_book_author = books[books['Book-Title'] == selected_book_title].iloc[0]['Book-Author']
        selected_book_image = books[books['Book-Title'] == selected_book_title].iloc[0]['Image-URL-M']
        st.markdown(f"<h3><b><span style='font-size: 20px;'>{selected_book_title}</span></b></h3>", unsafe_allow_html=True)
        st.text(selected_book_author)
        st.image(selected_book_image, width=150)

        # Display the rest of the recommended books
        recommendations = []
        for i, item in enumerate(similar_items):
            if i >= 10:  # Display up to 10 recommendations
                break
            if item[0] == index:  # Skip the selected book
                continue
            recommendations.append(item[0])

        recommendations_data = books.loc[recommendations, ['Book-Title', 'Book-Author', 'Image-URL-M']]
        recommendations_data.reset_index(drop=True, inplace=True)

        for i, row in recommendations_data.iterrows():
            with cols[i % 4]:
                book_title = row['Book-Title']
                book_author = row['Book-Author']
                book_image = row['Image-URL-M']
                st.markdown(f"<h4><span style='font-size: 16px;'>{book_title}</span></h4>", unsafe_allow_html=True)
                st.text(book_author)
                st.image(book_image, width=150)

    else:
        st.text("Book not found in the recommendation system.")

# Display popular books
st.subheader("Top 50 Popular Books")
cols_popular = st.columns(4)  # Adjust the number of columns as per your preference

for i in range(len(popular_df)):
    with cols_popular[i % 4]:
        st.markdown(f"<h4><span style='font-size: 16px;'>{popular_df['Book-Title'].iloc[i]}</span></h4>", unsafe_allow_html=True)
        st.text(popular_df['Book-Author'].iloc[i])
        st.image(popular_df['Image-URL-M'].iloc[i], width=150)
        st.text("Votes: " + str(popular_df['num_ratings'].iloc[i]))
        st.text("Average Rating: " + str(popular_df['avg_rating'].iloc[i]))
