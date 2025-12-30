
from manim import *
import numpy as np

class NTT(Scene):
    def construct(self):
        self.walkthrough()

    def walkthrough(self):
        # Configurações de estilo
        text_scale = 0.7
        space_y = 0.6
        
        # --- 1. Configuração Inicial ---
        # Mudamos de FFT para NTT
        first_call = MathTex(r"\text{NTT}([5, 3, 2, 1])")
        first_call.scale(0.8)
        first_call.to_corner(UL).shift(RIGHT * 1)
        
        first_call[0][4:7].set_color(BLUE)  # Índices pares
        first_call[0][8:-1].set_color(YELLOW) # Índices ímpares

        self.play(Write(first_call))

        P_x = MathTex("A(x) = 5 + 3x + 2x^2 + x^3").scale(text_scale)
        P_x.next_to(first_call, DOWN, buff=space_y).align_to(first_call, LEFT)
        self.play(Write(P_x))

        n_4 = MathTex("N = 4").scale(text_scale)
        n_4.next_to(P_x, DOWN, buff=space_y).align_to(P_x, LEFT)
        self.play(Write(n_4))

        # Aqui fazemos a conexão com a raiz primitiva do corpo finito
        omega_4 = MathTex(r"\psi^4 \equiv 1 \pmod p").scale(text_scale)
        omega_4.next_to(n_4, DOWN, buff=space_y).align_to(n_4, LEFT)
        self.play(Write(omega_4))
        self.wait()
        
        # Círculo das Potências (Raízes da Unidade no Corpo Finito)
        # Visualmente é um círculo, mas representa o ciclo gerado por psi
        w_i_values = MathTex("[1, \psi, \psi^2, \psi^3]").scale(text_scale)
        w_i_values.next_to(omega_4, RIGHT, buff=1.5)
        
        circle_group = self.create_unity_roots_circle(4, w_i_values.get_center())
        
        self.play(Write(w_i_values))
        self.wait()
        self.play(ReplacementTransform(w_i_values, circle_group))

        # Divisão Par/Ímpar (A_lo e A_hi implícitos)
        P_e = MathTex("A_{par}(x^2) = 5 + 2x", r"\rightarrow [5, 2]").scale(text_scale)
        P_e[1][-5:].set_color(ORANGE)
        P_e.next_to(omega_4, DOWN, buff=space_y).align_to(omega_4, LEFT)
        
        self.play(Write(P_e[0]))
        self.play(Write(P_e[1]))

        P_o = MathTex("A_{impar}(x^2) = 3 + x", r"\rightarrow [3, 1]").scale(text_scale)
        P_o[1][-5:].set_color(ORANGE)
        P_o.next_to(P_e, DOWN, buff=space_y).align_to(P_e, LEFT)
        
        self.play(Write(P_o[0]))
        self.play(Write(P_o[1]))
        self.wait()
        
        # Limpar tela para recursão
        self.play(
            FadeOut(P_x), FadeOut(n_4), FadeOut(omega_4), FadeOut(circle_group) 
        )

        # --- 2. Recursão (Árvore) ---
        
        left_call = MathTex(r"\text{NTT}([5, 2])").scale(0.8)
        left_call.move_to(LEFT * 3.5 + UP * 1.8)
        left_call[0][4:7].set_color(BLUE)
        left_call[0][8:-1].set_color(ORANGE)

        right_call = MathTex(r"\text{NTT}([3, 1])").scale(0.8)
        right_call.move_to(RIGHT * 3.5 + UP * 1.8)
        right_call[0][4:7].set_color(BLUE)
        right_call[0][8:-1].set_color(ORANGE)

        self.play(
            FadeOut(P_e), FadeOut(P_o),
            ReplacementTransform(P_e.copy(), left_call),
            ReplacementTransform(P_o.copy(), right_call)
        )

        # --- Ramo Esquerdo (N=2) ---
        P_x_left = MathTex("A(x) = 5 + 2x").scale(text_scale)
        P_x_left.next_to(left_call, DOWN, buff=space_y)
        
        n_2_left = MathTex("N = 2").scale(text_scale)
        n_2_left.next_to(P_x_left, DOWN, buff=space_y)

        # N=2 no corpo finito, a raiz é -1
        omega_2_left = MathTex(r"\psi^{N/2} \equiv -1").scale(text_scale)
        omega_2_left.next_to(n_2_left, DOWN, buff=space_y)

        self.play(Write(P_x_left), Write(n_2_left), Write(omega_2_left))

        # Círculo N=2
        circle_left_pos = n_2_left.get_center() + RIGHT * 2.5
        circle_left_group = self.create_unity_roots_circle(2, circle_left_pos, radius=0.5, color=ORANGE)
        self.play(FadeIn(circle_left_group))

        # Casos Base
        left_l_call = MathTex(r"\text{NTT}([5])", r"\rightarrow [5]").scale(text_scale)
        left_l_call.next_to(omega_2_left, DOWN, buff=1.5).shift(LEFT * 1.5)
        left_l_call[0][4:7].set_color(BLUE)
        left_l_call[1].set_color(GREEN)
        
        left_r_call = MathTex(r"\text{NTT}([2])", r"\rightarrow [2]").scale(text_scale)
        left_r_call.next_to(omega_2_left, DOWN, buff=1.5).shift(RIGHT * 1.5)
        left_r_call[0][4:7].set_color(BLUE)
        left_r_call[1].set_color(GREEN)

        self.play(Write(left_l_call), Write(left_r_call))
        self.wait()

        # Combinação (Butterfly) Esquerda
        y_e_l = MathTex("a_L = [5]").scale(text_scale).next_to(omega_2_left, DOWN, buff=space_y).align_to(omega_2_left, LEFT)
        y_o_l = MathTex("a_R = [2]").scale(text_scale).next_to(y_e_l, DOWN, buff=0.2).align_to(y_e_l, LEFT)
        VGroup(y_e_l, y_o_l).shift(UP * 0.2)
        
        self.play(Write(y_e_l), Write(y_o_l))

        y_left = MathTex("y = [0, 0]").scale(text_scale).next_to(y_o_l, DOWN, buff=0.5)
        self.play(Write(y_left))

        # Cálculos N=2
        # Mostra a soma simples pois psi^0 = 1
        y_calc = MathTex(r"y[0] = 5 + 2 = 7").scale(text_scale)
        y_calc.next_to(y_left, DOWN, buff=0.2)
        self.play(Write(y_calc), circle_left_group[1][0].animate.set_color(GREEN))
        
        y_left_res = MathTex("y = [7, 0]").scale(text_scale).move_to(y_left)
        self.play(Transform(y_left, y_left_res))
        
        # Mostra a subtração pois psi^{N/2} = -1
        y_calc2 = MathTex(r"y[1] = 5 - 2 = 3").scale(text_scale)
        y_calc2.move_to(y_calc)
        self.play(Transform(y_calc, y_calc2), circle_left_group[1][1].animate.set_color(GREEN))

        y_left_res = MathTex("y = [7, 3]").scale(text_scale).move_to(y_left)
        self.play(Transform(y_left, y_left_res))
        self.wait()

        left_result_arrow = MathTex(r"\rightarrow [7, 3]").scale(0.8).next_to(left_call, RIGHT)
        left_result_arrow.set_color(ORANGE)
        self.play(
            FadeOut(y_calc), FadeOut(y_e_l), FadeOut(y_o_l), 
            FadeOut(y_left), FadeOut(circle_left_group),
            FadeOut(P_x_left), FadeOut(n_2_left), FadeOut(omega_2_left),
            FadeOut(left_l_call), FadeOut(left_r_call),
            Write(left_result_arrow)
        )

        # --- Ramo Direito (N=2) ---
        # Simplificado para poupar tempo
        P_x_right = MathTex("A(x) = 3 + x").scale(text_scale).next_to(right_call, DOWN, buff=space_y)
        self.play(Write(P_x_right))

        right_res_text = MathTex(r"\rightarrow [4, 2]").scale(0.8).next_to(right_call, RIGHT)
        right_res_text.set_color(ORANGE)
        
        y_right_sim = MathTex("y = [4, 2]").scale(text_scale).next_to(P_x_right, DOWN)
        self.play(Write(y_right_sim))
        self.wait()

        self.play(
            FadeOut(y_right_sim), FadeOut(P_x_right),
            Write(right_res_text)
        )

        # --- 3. Combinação Final (N=4) ---
        self.play(
            FadeOut(left_call), FadeOut(left_result_arrow),
            FadeOut(right_call), FadeOut(right_res_text),
        )

        y_e_final = MathTex("a_L = [7, 3]").scale(text_scale)
        y_e_final.next_to(first_call, DOWN, buff=1.0).align_to(first_call, LEFT)
        y_e_final.set_color(ORANGE)

        y_o_final = MathTex("a_R = [4, 2]").scale(text_scale)
        y_o_final.next_to(y_e_final, DOWN, buff=0.2).align_to(y_e_final, LEFT)
        y_o_final.set_color(ORANGE)

        self.play(Write(y_e_final), Write(y_o_final))
        self.play(FadeIn(circle_group)) 

        y_final = MathTex("y = [0, 0, 0, 0]").scale(text_scale)
        y_final.next_to(circle_group, DOWN, buff=1)
        self.play(Write(y_final))

        calc_pos = y_final.get_center() + DOWN * 1.0

        # Esta é a parte CRUCIAL para a sua explicação:
        # Mostra o cálculo simbólico com psi em vez de números complexos
        
        # y[0] (psi^0 = 1)
        calc0 = MathTex(r"y[0] = 7 + 1 \cdot 4 = 11").scale(text_scale).move_to(calc_pos)
        self.play(Write(calc0), circle_group[1][0].animate.set_color(GREEN))
        self.play(Transform(y_final, MathTex("y = [11, 0, 0, 0]").scale(text_scale).move_to(y_final)))
        
        # y[2] (Simetria: -psi^0 = -1)
        calc2 = MathTex(r"y[2] = 7 - 1 \cdot 4 = 3").scale(text_scale).move_to(calc_pos)
        self.play(ReplacementTransform(calc0, calc2), circle_group[1][2].animate.set_color(GREEN))
        self.play(Transform(y_final, MathTex("y = [11, 0, 3, 0]").scale(text_scale).move_to(y_final)))

        # y[1] (Usa psi)
        # Aqui usamos notação simbólica para enfatizar a álgebra
        calc1 = MathTex(r"y[1] = 3 + \psi \cdot 2").scale(text_scale).move_to(calc_pos)
        self.play(ReplacementTransform(calc2, calc1), circle_group[1][1].animate.set_color(GREEN))
        self.play(Transform(y_final, MathTex(r"y = [11, 3+2\psi, 3, 0]").scale(text_scale).move_to(y_final)))

        # y[3] (Simetria: -psi)
        calc3 = MathTex(r"y[3] = 3 - \psi \cdot 2").scale(text_scale).move_to(calc_pos)
        self.play(ReplacementTransform(calc1, calc3), circle_group[1][3].animate.set_color(GREEN))
        self.play(Transform(y_final, MathTex(r"y = [11, 3+2\psi, 3, 3-2\psi]").scale(text_scale).move_to(y_final)))
        self.wait(2)

        # --- Finalização ---
        final_arrow = MathTex(r"\rightarrow [11, 3+2\psi, 3, 3-2\psi]").scale(0.8)
        final_arrow.next_to(first_call, RIGHT)
        final_arrow.set_color(YELLOW)

        self.play(
            FadeOut(calc3), FadeOut(y_final), FadeOut(y_e_final), FadeOut(y_o_final),
            circle_group.animate.scale(0.5).next_to(final_arrow, DOWN),
            Write(final_arrow)
        )
        self.wait(3)

    def create_unity_roots_circle(self, n, center, radius=0.8, color=YELLOW):
        circle = Circle(radius=radius, color=BLUE).move_to(center)
        dots = VGroup()
        labels = VGroup()
        
        for k in range(n):
            angle = k * (2 * np.pi / n)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            point = center + np.array([x, y, 0])

            dot = Dot(point=point, color=color, radius=0.06)
            dots.add(dot)

            # Labels adaptados para notação de potências de psi
            label_tex = ""
            if n == 2:
                label_tex = "1" if k == 0 else "-1"
            elif n == 4:
                if k == 0: label_tex = "1"
                elif k == 1: label_tex = r"\psi"
                elif k == 2: label_tex = r"\psi^2" # Equivalente a -1
                elif k == 3: label_tex = r"\psi^3" # Equivalente a -psi
            
            if label_tex:
                lbl = MathTex(label_tex).scale(0.5)
                direction = normalize(point - center)
                lbl.next_to(dot, direction, buff=0.1)
                labels.add(lbl)

        return VGroup(circle, dots, labels)