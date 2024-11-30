from manim import *
import numpy as np

HORIZONTAL_BUFFER = 1.2
VERTICAL_BUFFER = 1

e5_multiplication_table = [
    ["0", "3", "1", "4", "2"],
    ["3", "1", "4", "2", "0"],
    ["1", "4", "2", "0", "3"],
    ["4", "2", "0", "3", "1"],
    ["2", "0", "3", "1", "4"],
]

# e5_np = np.array(e5_multiplication_table)
# e5_rot_np = np.rot90(e5_np)

w5_multiplication_table = [
    ["0", "4", "3", "2", "1"],
    ["1", "0", "4", "3", "2"],
    ["2", "1", "0", "4", "3"],
    ["3", "2", "1", "0", "4"],
    ["4", "3", "2", "1", "0"],
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


def animate_move_to(
    entries: VGroup,
    pairs: list[tuple[int, int]],
) -> list[Mobject]:
    animations = []
    for source, target in pairs:
        from_entries = entries[source][1:]
        to_entries = entries[target][1:]
        animation = from_entries.animate.move_to(to_entries)
        animations.append(animation)
    return animations


def animate_pre_swap(
    table: Table, pairs: list[tuple[int, int]], is_rows: bool = True
) -> list[Mobject]:
    animations = []
    for source, target in pairs:
        if is_rows:
            start = table.get_entries((source + 1, 1)).get_left() + (0.1 * LEFT)
            end = table.get_entries((target + 1, 1)).get_left() + (0.1 * LEFT)
            angle = (target - source) * (TAU / 4)
        else:
            start = table.get_entries((1, source + 1)).get_top() + (0.1 * UP)
            end = table.get_entries((1, target + 1)).get_top() + (0.1 * UP)
            angle = -(target - source) * (TAU / 4)
        animations.append(
            Create(
                ArcBetweenPoints(
                    start=start, end=end, stroke_width=2, angle=angle
                ).add_tip(tip_shape=StealthTip, tip_length=0.1, tip_width=0.1)
            )
        )
    return animations


def indicate_tables(tables: list[Table]):
    return [Indicate(table.get_entries_without_labels()) for table in tables]


def show_heat_map(
    table: Table,
    row_swaps: list[tuple[int, int]],
    col_swaps: list[tuple[int, int]],
) -> list[Mobject]:
    animations = []
    for row, _ in enumerate(table.get_rows()):
        if row == 0:
            continue
        for col, _ in enumerate(table.get_columns()):
            if col == 0:
                continue
            val = 0
            for row_swap in row_swaps:
                if row == row_swap[0]:
                    val += abs(row_swap[0] - row_swap[1])
            for col_swap in col_swaps:
                if col == col_swap[0]:
                    val += abs(col_swap[0] - col_swap[1])
            print(row, col, val)
            cell = table.get_cell((row + 1, col + 1))
            bg_cell = BackgroundRectangle(cell, color=RED, fill_opacity=val / 5)
            animations.append(Create(bg_cell))
    return animations


class Rotation(Scene):
    def construct(self):
        e5 = (
            MobjectTable(
                table=to_mobject_table(e5_multiplication_table),
                row_labels=labels(),
                col_labels=labels(),
                top_left_entry=MathTex("E_5").scale(1.5),
                line_config={"stroke_width": 1, "color": BLUE},
                h_buff=HORIZONTAL_BUFFER,
                v_buff=VERTICAL_BUFFER,
            )
            .scale(0.5)
            .shift(3.5 * LEFT)  # TODO: center w/o magic numbers
        )

        w5 = MobjectTable(
            table=to_mobject_table(w5_multiplication_table),
            row_labels=labels(),
            col_labels=labels(),
            top_left_entry=MathTex("W_5").scale(1.3),
            line_config={"stroke_width": 1, "color": BLUE},
            h_buff=HORIZONTAL_BUFFER,
            v_buff=VERTICAL_BUFFER,
        ).scale(0.5)

        w5.next_to(e5, buff=2)
        self.play(e5.create())
        self.play(w5.create())

        rotate_grid_animations = []
        rotate_grid_animations.append(Rotate(e5.top_left_entry, angle=PI / 2))
        rotate_grid_animations.append(
            Rotate(e5.get_entries_without_labels(), angle=PI / 2)
        )
        self.play(rotate_grid_animations)
        self.wait()

        rotate_entries_animations = []
        for i in range(0, 5):
            for j in range(0, 5):
                rotate_entries_animations.append(
                    Rotate(e5.get_entries_without_labels((i, j)), angle=-PI / 2)
                )
        self.play(rotate_entries_animations)

        shift_animations = [e5.animate.shift(UP), w5.animate.shift(UP)]
        self.play(shift_animations)

        gamma_text = (
            VGroup(
                MathTex("0 \mapsto 4", color=RED),
                MathTex("1 \mapsto 2", color=RED),
                MathTex("2 \mapsto 0", color=RED),
                MathTex("3 \mapsto 3", color=RED),
                MathTex("4 \mapsto 1", color=RED),
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .scale(0.7)
        )
        gamma_text.next_to(e5, direction=DOWN).shift(0.2 * DOWN)
        self.add(gamma_text)

        # self.play(e5_rot.create())
        # self.play(FadeIn(e5_rot))
        # self.play(Transform(e5, e5_rot))
        self.wait()
        w5_copy = w5.copy()
        w5_copy.move_to(e5)
        self.play(FadeTransform(e5, w5_copy), run_time=3)
        self.wait()


class Isotopy(Scene):
    def construct(self):
        e5 = (
            MobjectTable(
                table=to_mobject_table(e5_multiplication_table),
                row_labels=labels(),
                col_labels=labels(),
                top_left_entry=MathTex("E_5").scale(1.5),
                line_config={"stroke_width": 1, "color": BLUE},
                h_buff=HORIZONTAL_BUFFER,
                v_buff=VERTICAL_BUFFER,
            )
            .scale(0.5)
            .shift(3.5 * LEFT)  # TODO: center w/o magic numbers
        )
        cells = e5.get_entries_without_labels()
        cells.set_color_by_gradient(BLUE, GREEN, YELLOW, RED)

        w5 = MobjectTable(
            table=to_mobject_table(w5_multiplication_table),
            row_labels=labels(),
            col_labels=labels(),
            top_left_entry=MathTex("W_5").scale(1.3),
            line_config={"stroke_width": 1, "color": BLUE},
            h_buff=HORIZONTAL_BUFFER,
            v_buff=VERTICAL_BUFFER,
        ).scale(0.5)

        w5.next_to(e5, buff=2)
        self.play(e5.create())
        self.play(w5.create())

        self.wait(2)
        rows_animations = animate_move_to(
            e5.get_rows(), [(1, 5), (2, 4), (4, 2), (5, 1)]
        )
        rows_animations.append(e5.top_left_entry.animate.flip(axis=[1, 0, 0]))
        self.play(rows_animations)

        self.wait(2)
        shift_animations = [e5.animate.shift(UP), w5.animate.shift(UP)]
        self.play(shift_animations)

        gamma_text = (
            VGroup(
                MathTex("0 \mapsto 4", color=RED),
                MathTex("1 \mapsto 2", color=RED),
                MathTex("2 \mapsto 0", color=RED),
                MathTex("3 \mapsto 3", color=RED),
                MathTex("4 \mapsto 1", color=RED),
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .scale(0.7)
        )
        gamma_text.next_to(e5, direction=DOWN).shift(0.2 * DOWN)
        self.add(gamma_text)

        self.wait(2)
        w5_copy = w5.copy()
        w5_copy.move_to(e5)
        self.play(FadeTransform(e5, w5_copy), run_time=3)
        self.wait()

        indicate_animations = indicate_tables([w5, w5_copy])
        self.play(indicate_animations)
        self.wait(2)


class PrincipalIsotopy(Scene):
    def construct(self):
        title = Text("Principal Isotopy", font="sans-serif")
        title.move_to([0, 3, 0])

        e5 = (
            MobjectTable(
                table=to_mobject_table(e5_multiplication_table),
                row_labels=labels(),
                col_labels=labels(),
                top_left_entry=MathTex("E_5").scale(1.5),
                line_config={"stroke_width": 1, "color": BLUE},
                h_buff=HORIZONTAL_BUFFER,
                v_buff=VERTICAL_BUFFER,
            )
            .scale(0.5)
            .shift(3.5 * LEFT)  # TODO: center w/o magic numbers
            .shift(DOWN)
        )
        e5_copy = e5.copy()
        cells = e5.get_entries_without_labels()
        cells.set_color_by_gradient(BLUE, GREEN, YELLOW, RED)
        e5_title = Tex("Equidistant quasigroup of order 5").scale(0.8)
        e5_title.next_to(e5, 3 * UP)

        w5 = MobjectTable(
            table=to_mobject_table(w5_multiplication_table),
            row_labels=labels(),
            col_labels=labels(),
            top_left_entry=MathTex("W_5").scale(1.3),
            line_config={"stroke_width": 1, "color": BLUE},
            h_buff=HORIZONTAL_BUFFER,
            v_buff=VERTICAL_BUFFER,
        ).scale(0.5)
        w5.next_to(e5, buff=2)
        w5_title = Tex("Ward quasigroup of $C_5$").scale(0.7)
        w5_title.next_to(w5, 3 * UP)

        self.play([Write(title, run_time=0.5), Write(e5_title), e5.create()])
        self.play([Write(w5_title), w5.create()])
        self.wait()

        row_swaps = [(2, 4), (3, 2), (4, 5), (5, 3)]
        pre_row_swap_animations = animate_pre_swap(e5, row_swaps)
        self.play(pre_row_swap_animations)
        self.wait()

        rows_animations = animate_move_to(e5.get_rows(), row_swaps)
        rows_animations.append(e5.top_left_entry.animate.flip(axis=[1, 0, 0]))
        self.play(rows_animations, run_time=2)
        self.wait(2)

        col_swaps = [(2, 3), (3, 5), (4, 2), (5, 4)]
        pre_col_swap_animations = animate_pre_swap(e5, col_swaps, is_rows=False)
        self.play(pre_col_swap_animations)
        self.wait()

        cols_animations = animate_move_to(e5.get_columns(), col_swaps)
        cols_animations.append(e5.top_left_entry.animate.flip())
        self.play(cols_animations, run_time=2)
        self.wait(1)

        indicate_animations = indicate_tables([e5, w5])
        self.play(indicate_animations)
        self.wait(3)

        heat_map_animations = show_heat_map(e5_copy, row_swaps, col_swaps)
        self.play(Transform(e5, e5_copy))
        self.play(heat_map_animations)
        self.wait(2)
