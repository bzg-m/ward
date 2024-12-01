from manim import *

HORIZONTAL_BUFFER = 1.2
VERTICAL_BUFFER = 1
LABEL_OFFSET = 1.3 * UP
LABEL_GROUP_OFFSET = 3 * UP

w5_multiplication_table = [
    ["0", "4", "3", "2", "1"],
    ["1", "0", "4", "3", "2"],
    ["2", "1", "0", "4", "3"],
    ["3", "2", "1", "0", "4"],
    ["4", "3", "2", "1", "0"],
]

d10_multiplication_table = [
    ["0", "4", "3", "2", "1", "0", "1", "2", "3", "4"],
    ["1", "0", "4", "3", "2", "4", "0", "1", "2", "3"],
    ["2", "1", "0", "4", "3", "3", "4", "0", "1", "2"],
    ["3", "2", "1", "0", "4", "2", "3", "4", "0", "1"],
    ["4", "3", "2", "1", "0", "1", "2", "3", "4", "0"],
]


def to_mobject_table(table: list[list[str]]) -> list[list[Mobject]]:
    table_obj = []
    for row in table:
        row_obj = []
        for val in row:
            val_obj = Tex(val, stroke_width=2).set(width=0.5, height=0.5)
            row_obj.append(val_obj)
        table_obj.append(row_obj)
    return table_obj


def labels() -> list[VMobject]:
    return [Text(str(i)) for i in range(0, 5)]


def d10_labels() -> list[VMobject]:
    labels = [
        "e",
        "r",
        "r^2",
        "r^3",
        "r^4",
        "s",
        "sr",
        "sr^2",
        "sr^3",
        "sr^4",
    ]
    return [MathTex(label).scale(0.9) for label in labels]


class Ward5(Scene):
    def construct(self):
        title = Tex("Isomorphism between $Mlt(W_5)$ and $D_{10}$")
        title.move_to([0, 3, 0])

        w5 = (
            MobjectTable(
                table=to_mobject_table(w5_multiplication_table),
                row_labels=labels(),
                col_labels=labels(),
                top_left_entry=MathTex("W_5").scale(1.3),
                line_config={"stroke_width": 1, "color": BLUE},
                h_buff=HORIZONTAL_BUFFER,
                v_buff=VERTICAL_BUFFER,
            )
            .scale(0.5)
            .shift(4 * LEFT)
            .shift(DOWN)
        )
        w5_title = Tex("Ward quasigroup of $C_5$").scale(0.7)
        w5_title.next_to(w5, UP)
        w5.get_entries_without_labels().set_color(BLUE)

        d10 = MobjectTable(
            table=to_mobject_table(d10_multiplication_table),
            row_labels=labels(),
            h_buff=HORIZONTAL_BUFFER,
            v_buff=VERTICAL_BUFFER,
        ).scale(0.45)
        d10.next_to(w5, buff=0.5)
        d10.get_entries_without_labels().set_color(BLUE)

        self.play([Write(title, run_time=0.5), Write(w5_title), w5.create()])
        self.wait()

        d10_labels_local = d10_labels()

        lq = (
            MathTex("L(q)", color=RED)
            .scale(0.9)
            .next_to(d10.get_columns()[1], LABEL_GROUP_OFFSET)
        )
        self.play(Write(lq))
        for i in range(1, 6):
            w5_col_copy = w5.get_columns()[i][1:].copy()
            d10_col = d10.get_columns()[i]
            label = d10_labels_local[i - 1]
            label.next_to(d10_col, LABEL_OFFSET)
            self.play(
                Transform(w5_col_copy, d10_col),
                Write(label, rate_func=rate_functions.rush_into),
            )
        self.wait()

        rq = (
            MathTex("R(q)", color=RED)
            .scale(0.9)
            .next_to(d10.get_columns()[6], LABEL_GROUP_OFFSET)
        )
        self.play(Write(rq))
        for i in range(1, 6):
            w5_row_copy = w5.get_rows()[i].copy()
            d10_col = d10.get_columns()[i + 5]
            label = d10_labels_local[i + 5 - 1]
            label.next_to(d10_col, LABEL_OFFSET)
            self.play(
                Transform(w5_row_copy, d10_col),
                Write(label, rate_func=rate_functions.rush_into),
            )
        self.wait()

        self.play(Write(d10.get_row_labels()))
        self.wait(3)
