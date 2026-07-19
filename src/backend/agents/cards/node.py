from agents.cards.mapping import extract_cards_from_messages


async def img_node(state):
    taro_cards, unlock_name = extract_cards_from_messages(state["messages"])
    return {
        "taro_cards": taro_cards,
        "next_node": "add_memory",
        "unlock_name": unlock_name,
    }
