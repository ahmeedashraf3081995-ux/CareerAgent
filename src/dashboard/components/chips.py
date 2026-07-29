import streamlit as st



def process_input(key):

    input_key = f"{key}_input"


    value = st.session_state.get(
        input_key,
        ""
    )


    if value.strip():


        current_values = st.session_state.get(
            key,
            []
        )


        values = (
            value
            .replace("\n", ",")
            .split(",")
        )


        for item in values:

            item = item.strip()


            if item and item not in current_values:

                current_values.append(item)



        st.session_state[key] = current_values



    st.session_state[input_key] = ""




def remove_value(key, item):

    if item in st.session_state.get(key, []):

        st.session_state[key].remove(item)




def tag_input(label, key):


    # Initialize

    if key not in st.session_state:

        st.session_state[key] = []



    st.markdown(
        f"**{label}**"
    )



    input_key = f"{key}_input"



    if input_key not in st.session_state:

        st.session_state[input_key] = ""



    # Input

    st.text_input(
        "Type and press Enter",
        key=input_key,
        on_change=process_input,
        args=(key,),
        placeholder=f"Add {label.lower()}"
    )



    if st.button(
        "➕ Add",
        key=f"add_button_{key}"
    ):

        process_input(key)

        st.rerun()



    # Display chips

    values = st.session_state.get(
        key,
        []
    )


    if values:


        st.caption(
            "Selected:"
        )


        cols = st.columns(4)



        for i, item in enumerate(
            list(values)
        ):


            with cols[i % 4]:


                if st.button(
                    f"❌ {item}",
                    key=f"remove_{key}_{i}"
                ):


                    remove_value(
                        key,
                        item
                    )


                    st.rerun()



    return values