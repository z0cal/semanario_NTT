from manim import *

class NTT_Full_Story_Continuous(Scene):
    def construct(self):
        # ============================================
        # PARTE 1: DIAGRAMA BUTTERFLY (LADO DIREITO)
        # ============================================
        
        # Configurações de layout
        row_height = 1.5
        col_width = 3.5
        start_x = -2.0 
        
        rows = [1.5 * row_height, 0.5 * row_height, -0.5 * row_height, -1.5 * row_height]
        
        title = Tex(r"NTT ($N=4$) ").to_edge(UP)
        self.play(Write(title), run_time=1.0)
        
        inputs = VGroup(*[MathTex(f"x[{i}]") for i in range(4)])
        for i, item in enumerate(inputs):
            item.move_to([start_x, rows[i], 0])
        
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT) for i in inputs], lag_ratio=0.5))

        # Lista VIP: Estes objetos serão preservados
        self.all_twiddles = VGroup()

        def create_butterfly_stage(start_pos_x, line_indices, twiddles):
            elements = VGroup()
            x_base = start_pos_x
            x_end = start_pos_x + col_width
            
            for top, bot in line_indices:
                top_y = rows[top]
                bot_y = rows[bot]
                
                # Linhas e círculos (não são VIPs)
                l1 = Line([x_base, top_y, 0], [x_base + 1, top_y, 0])
                l2 = Line([x_base, bot_y, 0], [x_base + 1, bot_y, 0])
                elements.add(l1, l2)
                
                butterfly_start_x = x_base + 1
                
                # Twiddles
                if bot in twiddles:
                    mult_circle = Circle(radius=0.25, color=BLUE, fill_opacity=0.2).move_to([x_base + 1, bot_y, 0])
                    mult_tex = MathTex(r"\times").scale(0.5).move_to(mult_circle.get_center())
                    
                    # O Label PSI (Este é VIP!)
                    psi_label = MathTex(twiddles[bot], color=YELLOW).next_to(mult_circle, DOWN, buff=0.1).scale(0.8)
                    self.all_twiddles.add(psi_label) # Adiciona à lista de preservação
                    
                    elements.add(mult_circle, mult_tex, psi_label)
                    butterfly_start_x = x_base + 1.25
                
                # Nós, símbolos e setas (não são VIPs)
                sum_node = Circle(radius=0.25, color=GREEN).move_to([x_end - 0.5, top_y, 0])
                sub_node = Circle(radius=0.25, color=RED).move_to([x_end - 0.5, bot_y, 0])
                elements.add(sum_node, sub_node, MathTex("+").scale(0.5).move_to(sum_node), MathTex("-").scale(0.5).move_to(sub_node))
                
                elements.add(Arrow([butterfly_start_x, top_y, 0], sum_node.get_left(), buff=0.05))
                elements.add(Arrow([butterfly_start_x, top_y, 0], sub_node.get_left(), buff=0.05))
                elements.add(Arrow([butterfly_start_x, bot_y, 0], sum_node.get_left(), buff=0.05))
                elements.add(Arrow([butterfly_start_x, bot_y, 0], sub_node.get_left(), buff=0.05))
                
                elements.add(Line(sum_node.get_right(), [x_end, top_y, 0]), Line(sub_node.get_right(), [x_end, bot_y, 0]))

            return elements

        # Desenhar Estágios
        stage1 = create_butterfly_stage(start_x + 0.5, [(0, 2), (1, 3)], {2: r"\psi^2", 3: r"\psi^2"})
        self.play(LaggedStart(*[Create(obj) for obj in stage1], lag_ratio=0.05, run_time=3))
        
        stage2 = create_butterfly_stage(start_x + col_width + 0.5, [(0, 1), (2, 3)], {1: r"\psi^1", 3: r"\psi^3"})
        self.play(LaggedStart(*[Create(obj) for obj in stage2], lag_ratio=0.05, run_time=3))

        # Saídas
        outputs = VGroup()
        for i, label in enumerate([r"X_0", r"X_2", r"X_1", r"X_3"]):
            tex = MathTex(label).move_to([start_x + 2*col_width + 1.0, rows[i], 0])
            outputs.add(tex, Arrow([start_x + 2*col_width + 0.5, rows[i], 0], tex.get_left(), buff=0.1))
        self.play(Write(outputs))
        self.wait(1)

        # ============================================
        # PARTE 2: TRANSIÇÃO (FADE OUT SELETIVO)
        # ============================================
        
        # Lógica robusta: Criar um grupo com tudo que NÃO for um twiddle VIP
        stuff_to_fade = VGroup(title, inputs, outputs)
        
        # Iterar pelos estágios e pegar tudo que não está na lista VIP
        for mob in stage1:
            if mob not in self.all_twiddles:
                stuff_to_fade.add(mob)
        for mob in stage2:
            if mob not in self.all_twiddles:
                stuff_to_fade.add(mob)
        
        # Apagar o resto. Os twiddles originais ficam na tela nas suas posições.
        self.play(FadeOut(stuff_to_fade), run_time=1.5)
        
        # --- MOVER OS OBJETOS RESTANTES ---
        
        list_title = Tex("Raízes no Diagrama:", color=YELLOW).to_edge(LEFT).shift(UP*2)
        self.play(Write(list_title))
        
        base_list_pos = list_title.get_bottom() + RIGHT * 1.0
        
        target_positions = [
            base_list_pos + DOWN * 1.0, # psi^2
            base_list_pos + DOWN * 1.0, # psi^2 (overlap)
            base_list_pos + DOWN * 2.5, # psi^1
            base_list_pos + DOWN * 4.0  # psi^3
        ]
        
        anims = []
        # A ordem em all_twiddles é: [psi^2(s1), psi^2(s1), psi^1(s2), psi^3(s2)]
        
        # Usa os PRÓPRIOS objetos que sobraram na tela para a animação
        # psi^2 (primeiro)
        anims.append(self.all_twiddles[0].animate.move_to(target_positions[0]).scale(1.5))
        # psi^2 (segundo) - move para o mesmo lugar e desaparece
        anims.append(self.all_twiddles[1].animate.move_to(target_positions[0]).set_opacity(0)) 
        # psi^1
        anims.append(self.all_twiddles[2].animate.move_to(target_positions[2]).scale(1.5))
        # psi^3
        anims.append(self.all_twiddles[3].animate.move_to(target_positions[3]).scale(1.5))
        
        self.play(*anims, run_time=2)
        
        # Referências para conectar depois (usando os objetos que acabaram de se mover)
        ref_psi2 = self.all_twiddles[0]
        ref_psi1 = self.all_twiddles[2]
        ref_psi3 = self.all_twiddles[3]

        # ============================================
        # PARTE 3: BIT REVERSAL (LADO DIREITO/CENTRO)
        # ============================================
        
        br_title = Tex(r"\textbf{Bit Reversal Logic}", color=BLUE).move_to(UP*3 + RIGHT*2)
        formula = MathTex(r"\text{Exp} = \text{rev}_2(2^s + i)").next_to(br_title, DOWN)
        self.play(Write(br_title), Write(formula))
        
        block_center = RIGHT * 2.5
        
        # 1. Caso Stage 0 (Gera psi^2) -> Conecta ao objeto ref_psi2
        self.run_bit_rev_case(0, 0, 1, "0", "1", 2, block_center, YELLOW, ref_psi2)
        
        # 2. Caso Stage 1, i=0 (Gera psi^1) -> Conecta ao objeto ref_psi1
        self.run_bit_rev_case(1, 0, 2, "1", "0", 1, block_center, GREEN, ref_psi1)
        
        # 3. Caso Stage 1, i=1 (Gera psi^3) -> Conecta ao objeto ref_psi3
        self.run_bit_rev_case(1, 1, 3, "1", "1", 3, block_center, ORANGE, ref_psi3)

        self.wait(3)

    def run_bit_rev_case(self, stage, index, val, msb, lsb, res, center, color, target_root):
        group = VGroup()
        label = MathTex(rf"s={stage}, i={index} \quad (\text{{Base }} 2^{stage} + {index} = {val})").set_color(color).move_to(center + UP*0.5)
        group.add(label)
        
        b_msb = MathTex(msb, color=RED).scale(2).move_to(center + LEFT*0.6 + DOWN*0.5)
        b_lsb = MathTex(lsb, color=BLUE).scale(2).move_to(center + RIGHT*0.6 + DOWN*0.5)
        boxes = VGroup(SurroundingRectangle(b_msb, color=GRAY), SurroundingRectangle(b_lsb, color=GRAY))
        
        self.play(FadeIn(label), Create(boxes), Write(b_msb), Write(b_lsb))
        group.add(boxes, b_msb, b_lsb)
        
        arrow = MathTex(r"\downarrow").move_to(center + DOWN*1.5)
        self.play(FadeIn(arrow))
        group.add(arrow)
        
        t_msb, t_lsb = b_msb.copy(), b_lsb.copy()
        target_y = center[1] + -2.5
        self.play(
            t_lsb.animate(path_arc=-1.5).move_to([center[0] - 0.6, target_y, 0]),
            t_msb.animate(path_arc=1.5).move_to([center[0] + 0.6, target_y, 0]),
            run_time=1.5
        )
        group.add(t_msb, t_lsb)
        
        final_box = SurroundingRectangle(VGroup(t_lsb, t_msb), color=color, buff=0.2)
        res_text = MathTex(rf"= {res} \to \psi^{res}").next_to(final_box, RIGHT)
        
        self.play(Create(final_box), Write(res_text))
        group.add(final_box, res_text)
        
        # CONEXÃO: Seta sai do resultado e aponta para a raiz que se moveu anteriormente
        connection = Arrow(res_text.get_left(), target_root.get_right(), color=color, buff=0.1)
        self.play(Create(connection))
        self.play(Indicate(target_root, color=color, scale_factor=1.2))
        self.wait(1)
        
        self.play(FadeOut(group), FadeOut(connection))