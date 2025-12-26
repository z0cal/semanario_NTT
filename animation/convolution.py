from manim import *

class ConvolutionMatrixVsSum(Scene):
    def construct(self):
        # ==========================================
        # PARTE 1: MÉTODO MATRICIAL
        # ==========================================
        
        # --- 1. Configurações ---
        title = Title(r"Comparação: Matriz ($C_x \cdot y$) vs Somatório ($\sum$)")
        self.add(title)

        x_tex = ["x_0", "x_1", "x_2"]
        y_tex = ["y_0", "y_1", "y_2"]

        # Vetor x inicial
        x_col = Matrix([[xi] for xi in x_tex]).set_color(BLUE).scale(0.8)
        lbl_x = MathTex("x = ").next_to(x_col, LEFT)
        
        group_x = VGroup(lbl_x, x_col).to_edge(LEFT, buff=1.0)
        self.play(Write(group_x))
        self.wait(0.5)

        # --- 2. Matriz Cx ---
        rows = [
            ["x_0", "x_2", "x_1"],
            ["x_1", "x_0", "x_2"],
            ["x_2", "x_1", "x_0"]
        ]
        cx_matrix = Matrix(rows).set_color(BLUE).scale(0.8)
        lbl_cx_target = MathTex("C_x = ").scale(0.8).next_to(cx_matrix, LEFT)

        # Transformação
        target_col0 = cx_matrix.get_columns()[0].get_center()
        self.play(
            lbl_x.animate.become(lbl_cx_target),
            x_col.animate.move_to(target_col0)
        )
        self.play(Create(cx_matrix.get_brackets()))

        # Shifts
        col1 = cx_matrix.get_columns()[1]
        col2 = cx_matrix.get_columns()[2]
        self.play(TransformFromCopy(x_col, col1), run_time=0.6)
        self.play(TransformFromCopy(col1, col2), run_time=0.6)

        # --- 3. Equação Matricial Completa ---
        y_vec = Matrix([[yi] for yi in y_tex]).set_color(YELLOW).scale(0.8)
        dot = MathTex(r"\cdot").scale(1.2)
        eq = MathTex("=").scale(1.2)
        
        # Resultado da Matriz
        res_rows = [
            [r"x_0 y_0 + x_2 y_1 + x_1 y_2"],
            [r"x_1 y_0 + x_0 y_1 + x_2 y_2"],
            [r"x_2 y_0 + x_1 y_1 + x_0 y_2"]
        ]
        res_matrix = Matrix(res_rows).scale(0.65).set_color(WHITE)

        # Grupo e Posição
        matrix_group = VGroup(cx_matrix, dot, y_vec, eq, res_matrix)
        matrix_group.arrange(RIGHT, buff=0.15)
        matrix_group.move_to(ORIGIN).shift(DOWN * 0.5)

        shift_vector = matrix_group[0].get_center() - cx_matrix.get_center()
        
        self.play(
            cx_matrix.animate.shift(shift_vector),
            FadeOut(lbl_x), 
            FadeOut(x_col),
            run_time=0.8
        )

        self.play(Write(dot), Write(y_vec), Write(eq))
        self.play(Create(res_matrix.get_brackets()))

        # Multiplicação (Rápida)
        rows_m = cx_matrix.get_rows()
        col_y = y_vec.get_columns()[0]
        res_rows_mob = res_matrix.get_rows()

        for i in range(3):
            self.play(Write(res_rows_mob[i]), run_time=0.3)

        self.wait(1)

        # ==========================================
        # PARTE 2: PREPARAÇÃO PARA COMPARAÇÃO
        # ==========================================

        # Agrupa tudo da parte matricial (exceto título)
        full_matrix_scene = VGroup(matrix_group, res_matrix.get_brackets())
        
        # Label para identificar este método
        lbl_method_1 = Text("Método 1: Operador", font_size=20, color=BLUE)
        lbl_method_1.next_to(full_matrix_scene, UP)
        
        group_method_1 = VGroup(lbl_method_1, full_matrix_scene)

        self.play(
            group_method_1.animate.scale(0.7).to_edge(UP, buff=1.2)
        )
        
        # Linha separadora
        separator = Line(LEFT*6, RIGHT*6, color=GRAY).next_to(group_method_1, DOWN, buff=0.3)
        self.play(Create(separator))

        # ==========================================
        # PARTE 3: MÉTODO DA DEFINIÇÃO (Somatório)
        # ==========================================
        
        # Fórmula: y[k] = sum x[i] * y[k-i]
        def_tex = MathTex(
            r"\text{Método 2: Definição } \quad y[k] = \sum_{i=0}^{2} x[i] \cdot y[(k-i)_3]"
        ).scale(0.8).next_to(separator, DOWN, buff=0.3)
        
        self.play(Write(def_tex))

        # Vamos expandir termo a termo para k=0, 1, 2
        eq_k0 = MathTex(
            r"k=0: \quad x_0 y_0 + x_1 y_2 + x_2 y_1"
        ).scale(0.7)
        
        eq_k1 = MathTex(
            r"k=1: \quad x_0 y_1 + x_1 y_0 + x_2 y_2"
        ).scale(0.7)
        
        eq_k2 = MathTex(
            r"k=2: \quad x_0 y_2 + x_1 y_1 + x_2 y_0"
        ).scale(0.7)

        sum_group = VGroup(eq_k0, eq_k1, eq_k2).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        sum_group.next_to(def_tex, DOWN, buff=0.5)

        self.play(Write(sum_group))
        self.wait(1)

        # ==========================================
        # PARTE 4: COMPARAÇÃO FINAL
        # ==========================================
        
        matrix_res_rows = res_matrix.get_rows() 

        for i, sum_row in enumerate(sum_group):
            # Caixa ao redor da linha da matriz
            rect_matrix = SurroundingRectangle(matrix_res_rows[i], color=GREEN, buff=0.05)
            # Caixa ao redor da linha do somatório
            rect_sum = SurroundingRectangle(sum_row, color=GREEN, buff=0.05)
            
            # Seta conectando
            arrow = Arrow(rect_matrix.get_bottom(), rect_sum.get_top(), color=GREEN, buff=0.1)
            
            self.play(
                Create(rect_matrix),
                Create(rect_sum),
                GrowArrow(arrow),
                run_time=0.5
            )
            
            # Texto de "Igual"
            check = MathTex(r"\checkmark", color=GREEN).next_to(rect_sum, RIGHT)
            self.play(FadeIn(check, scale=0.5), run_time=0.3)
            
            self.wait(0.5)
            
            # Limpa para a próxima linha
            self.play(
                FadeOut(rect_matrix),
                FadeOut(rect_sum),
                FadeOut(arrow),
                run_time=0.2
            )



        self.wait(3)