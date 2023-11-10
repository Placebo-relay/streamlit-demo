import streamlit as st

class Money:
    MAX_SHILLINGS = 20
    MAX_PENCE = 12
    
    def __init__(self, pounds, shillings, pence):
        self.pounds = pounds
        self.shillings = shillings
        self.pence = pence
    
    def is_valid(self):
        return (
            0 <= self.pounds < Money.MAX_SHILLINGS and
            0 <= self.shillings < Money.MAX_SHILLINGS and
            0 <= self.pence < Money.MAX_PENCE
        )
    
    def increase(self, pounds=0, shillings=0, pence=0):
        self.pounds += pounds
        self.shillings += shillings
        self.pence += pence
        
        # Adjust
        self.shillings += self.pence // Money.MAX_PENCE
        self.pence %= Money.MAX_PENCE
        
        self.pounds += self.shillings // Money.MAX_SHILLINGS
        self.shillings %= Money.MAX_SHILLINGS
    
    def add(self, other):
        total_pence = self.to_pence() + other.to_pence()
        return Money.from_pence(total_pence)
    
    def subtract(self, other):
        total_pence = self.to_pence() - other.to_pence()
        return Money.from_pence(total_pence)
    
    def to_pence(self):
        return self.pounds * Money.MAX_SHILLINGS * Money.MAX_PENCE + \
               self.shillings * Money.MAX_PENCE + \
               self.pence
    
    def from_pence(total_pence):
        pounds = total_pence // (Money.MAX_SHILLINGS * Money.MAX_PENCE)
        total_pence %= (Money.MAX_SHILLINGS * Money.MAX_PENCE)
        
        shillings = total_pence // Money.MAX_PENCE
        pence = total_pence % Money.MAX_PENCE
        
        return Money(pounds, shillings, pence)
    
    def __str__(self):
        return f"{self.pounds}-{self.shillings}-{self.pence:02d}"
    
    def __repr__(self):
        return f"{self.pounds}-{self.shillings}-{self.pence:02d}"
        

def find_average(money_list):
    total_pence = sum(money.to_pence() for money in money_list)
    average_pence = total_pence // len(money_list)
    return average_pence, Money.from_pence(average_pence)


def find_closest_and_farthest(money_list):
    closest_pairs = []
    farthest_pairs = []
    min_diff = float('inf')
    max_diff = float('-inf')
    
    for i in range(len(money_list)):
        for j in range(i + 1, len(money_list)):
            diff = abs(money_list[i].to_pence() - money_list[j].to_pence())
            if diff < min_diff:
                min_diff = diff
                closest_pairs = [(money_list[i], money_list[j])]
            elif diff == min_diff:
                closest_pairs.append((money_list[i], money_list[j]))
                
            if diff > max_diff:
                max_diff = diff
                farthest_pairs = [(money_list[i], money_list[j])]
            elif diff == max_diff:
                farthest_pairs.append((money_list[i], money_list[j]))
    
    return closest_pairs, farthest_pairs


def main():
    hide_menu = """
    <style>
    header {
        visibility: visible;
    }
    #MainMenu {
        visibility: visible;
    }
    
    footer {
        visibility: hidden;
    }
    footer:after{
        visibility: visible;
        Content:"Demo of money-list. Copyright @ 2023";
        display: block;
        position: relative;
        padding: 5px;
        top:3px;
        color: tomato;
        text-align: left;
    </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)
    st.title("Money List App")
    
    st.write("Here is the currency conversion information:")
    st.write("- a shilling is equal to", Money.MAX_PENCE, "pence")
    st.write("- a pound is equal to", Money.MAX_SHILLINGS, "shillings")
    
    money_list = []
    money_pence_list = []
    
    input_text = st.text_area("Enter money (one per line):")
    collect_button = st.button("Collect List")

    if collect_button:
    
        money_inputs = input_text.strip().split("\n")
        for money_input in money_inputs:
            money_input = money_input.strip()
            if money_input:
                money_parts = money_input.split("-")
                if len(money_parts) == 1:
                    pence = int(money_parts[0])
                    new_money = Money.from_pence(pence)
                elif len(money_parts) == 3:
                    pence = int(money_parts[0])*12*20+int(money_parts[1])*12+int(money_parts[2])
                    new_money = Money.from_pence(pence)
                else:
                    st.write(f"Invalid input: {money_input}")
                    continue
                
                money_list.append(new_money)
                money_pence_list.append(pence)
        
        if money_list:
            st.sidebar.write("Pound-Shilling-Pence List:",money_list)
            st.sidebar.write("Pence List:",money_pence_list)
            total_sum = Money(0,0,sum(money.to_pence() for money in money_list))
            avrg = find_average(money_list)
            st.sidebar.write("Total", total_sum.pence, '=', Money.from_pence(total_sum.pence))
            st.sidebar.write("Average", avrg[0],'=',avrg[1])
            
            st.sidebar.write("[Closest],[Farthest] pairs",find_closest_and_farthest(money_list))
        
    body = """import streamlit as st

class Money:
    MAX_SHILLINGS = 20
    MAX_PENCE = 12
    
    def __init__(self, pounds, shillings, pence):
        self.pounds = pounds
        self.shillings = shillings
        self.pence = pence
    
    def is_valid(self):
        return (
            0 <= self.pounds < Money.MAX_SHILLINGS and
            0 <= self.shillings < Money.MAX_SHILLINGS and
            0 <= self.pence < Money.MAX_PENCE
        )
    
    def increase(self, pounds=0, shillings=0, pence=0):
        self.pounds += pounds
        self.shillings += shillings
        self.pence += pence
        
        # Adjust
        self.shillings += self.pence // Money.MAX_PENCE
        self.pence %= Money.MAX_PENCE
        
        self.pounds += self.shillings // Money.MAX_SHILLINGS
        self.shillings %= Money.MAX_SHILLINGS
    
    def add(self, other):
        total_pence = self.to_pence() + other.to_pence()
        return Money.from_pence(total_pence)
    
    def subtract(self, other):
        total_pence = self.to_pence() - other.to_pence()
        return Money.from_pence(total_pence)
    
    def to_pence(self):
        return self.pounds * Money.MAX_SHILLINGS * Money.MAX_PENCE + \
               self.shillings * Money.MAX_PENCE + \
               self.pence
    
    def from_pence(total_pence):
        pounds = total_pence // (Money.MAX_SHILLINGS * Money.MAX_PENCE)
        total_pence %= (Money.MAX_SHILLINGS * Money.MAX_PENCE)
        
        shillings = total_pence // Money.MAX_PENCE
        pence = total_pence % Money.MAX_PENCE
        
        return Money(pounds, shillings, pence)
    
    def __str__(self):
        return f"{self.pounds}-{self.shillings}-{self.pence:02d}"
    
    def __repr__(self):
        return f"{self.pounds}-{self.shillings}-{self.pence:02d}"
        

def find_average(money_list):
    total_pence = sum(money.to_pence() for money in money_list)
    average_pence = total_pence // len(money_list)
    return average_pence, Money.from_pence(average_pence)


def find_closest_and_farthest(money_list):
    closest_pairs = []
    farthest_pairs = []
    min_diff = float('inf')
    max_diff = float('-inf')
    
    for i in range(len(money_list)):
        for j in range(i + 1, len(money_list)):
            diff = abs(money_list[i].to_pence() - money_list[j].to_pence())
            if diff < min_diff:
                min_diff = diff
                closest_pairs = [(money_list[i], money_list[j])]
            elif diff == min_diff:
                closest_pairs.append((money_list[i], money_list[j]))
                
            if diff > max_diff:
                max_diff = diff
                farthest_pairs = [(money_list[i], money_list[j])]
            elif diff == max_diff:
                farthest_pairs.append((money_list[i], money_list[j]))
    
    return closest_pairs, farthest_pairs


def main():
    st.title("Money List App")
    
    st.write("Here is the currency conversion information:")
    st.write("- a shilling is equal to", Money.MAX_PENCE, "pence")
    st.write("- a pound is equal to", Money.MAX_SHILLINGS, "shillings")
    
    money_list = []
    money_pence_list = []
    
    input_text = st.text_area("Enter money (one per line):")
    collect_button = st.button("Collect List")

    if collect_button:
    
        money_inputs = input_text.strip().split("\n")
        for money_input in money_inputs:
            money_input = money_input.strip()
            if money_input:
                money_parts = money_input.split("-")
                if len(money_parts) == 1:
                    pence = int(money_parts[0])
                    new_money = Money.from_pence(pence)
                elif len(money_parts) == 3:
                    pence = int(money_parts[0])*12*20+int(money_parts[1])*12+int(money_parts[2])
                    new_money = Money.from_pence(pence)
                else:
                    st.write(f"Invalid input: {money_input}")
                    continue
                
                money_list.append(new_money)
                money_pence_list.append(pence)
        
        if money_list:
            st.sidebar.write("Pound-Shilling-Pence List:",money_list)
            st.sidebar.write("Pence List:",money_pence_list)
            total_sum = Money(0,0,sum(money.to_pence() for money in money_list))
            avrg = find_average(money_list)
            st.sidebar.write("Total", total_sum.pence, '=', Money.from_pence(total_sum.pence))
            st.sidebar.write("Average", avrg[0],'=',avrg[1])
            
            st.sidebar.write("[Closest],[Farthest] pairs",find_closest_and_farthest(money_list))
            """
            
    st.code(body, language="python", line_numbers=False)
    
if __name__ == "__main__":
    main()
