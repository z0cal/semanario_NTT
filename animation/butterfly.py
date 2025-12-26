from manim import *

class FFTButterfly4Points(Scene):
    def construct(self):
        # --- Configurações Gerais ---
        title = Title(r"FFT 4-Pontos: Operação Butterfly (DIT)")
        self.add(title)
        
        # Posições (Grid)
        # Colunas: Inputs, Stage1, Outputs
        col_x = [-5, -1, 3] 
        # Linhas: 0, 1, 2, 3 (De cima para baixo)
        row_y = [2.5, 1.0, -1.0, -2.5]
        
        # --- 1. Inputs (Bit Reversed Order) ---
        # Ordem para N=4 DIT: 0 (00), 2 (10), 1 (01), 3 (11)
        indices = [0, 2, 1, 3]
        
        input_nodes = VGroup()
        input_labels = VGroup()
        
        for i, idx in enumerate(indices):
            dot = Dot(point=[col_x[0], row_y[i], 0], color=BLUE)
            label = MathTex(f"x[{idx}]").next_to(dot, LEFT)
            input_nodes.add(dot)
            input_labels.add(label)
            
        header_in = Text("Entrada (Bit-Rev)", font_size=20, color=BLUE).next_to(input_nodes, UP, buff=0.5)
        
        self.play(
            FadeIn(header_in),
            LaggedStart(*[Write(l) for l in input_labels], lag_ratio=0.2),
            LaggedStart(*[Create(d) for d in input_nodes], lag_ratio=0.2)
        )
        self.wait(0.5)

        # --- Helper para desenhar uma Butterfly Unit ---
        def create_butterfly(start_col_idx, top_row_idx, span, weight_tex, color=WHITE):
            """
            Cria uma estrutura butterfly padrão:
            A ----> A + W*B
            B --X-> A - W*B (ou similar, dependendo da convenção)
            Aqui usaremos a visualização gráfica padrão:
            Linhas retas horizontais e linhas diagonais cruzadas.
            O peso (zeta) geralmente é aplicado na 'perna' de baixo antes de cruzar.
            """
            x_start = col_x[start_col_idx]
            x_end = col_x[start_col_idx + 1]
            
            y_top = row_y[top_row_idx]
            y_bot = row_y[top_row_idx + span]
            
            # Nós de origem e destino
            p_top_start = np.array([x_start, y_top, 0])
            p_bot_start = np.array([x_start, y_bot, 0])
            p_top_end   = np.array([x_end, y_top, 0])
            p_bot_end   = np.array([x_end, y_bot, 0])
            
            # Linhas
            # 1. Topo direto (Horizontal)
            l1 = Line(p_top_start, p_top_end, color=color)
            # 2. Baixo direto (Horizontal)
            l2 = Line(p_bot_start, p_bot_end, color=color)
            # 3. Cruzamento Baixo -> Topo
            l3 = Line(p_bot_start, p_top_end, color=color)
            # 4. Cruzamento Topo -> Baixo
            l4 = Line(p_top_start, p_bot_end, color=color)
            
            lines = VGroup(l1, l2, l3, l4)
            
            # Label do peso (Twiddle Factor)
            # Geralmente colocado perto da origem da perna inferior
            w_label = MathTex(weight_tex, color=ORANGE, font_size=28)
            # Posiciona um pouco acima da linha de baixo, perto do início
            w_label.next_to(p_bot_start, UR, buff=0.1).shift(RIGHT*0.5)
            
            # Marcador de -1 (subtração) na chegada da diagonal inferior
            # Convenção comum: A perna de cima soma, a de baixo subtrai no cruzamento
            neg_label = MathTex("-1", font_size=20, color=RED).move_to(l4.point_from_proportion(0.85)).shift(UP*0.2)
            
            return lines, w_label, neg_label

        # --- 2. Estágio 1 (Combinar pares de 2 pontos) ---
        # Borboletas span=1 (vizinhas)
        # N=2, twiddle é zeta_2^0 = 1
        
        stage1_header = Text("Estágio 1 (N=2)", font_size=20, color=YELLOW).move_to([col_x[1], 3.5, 0])
        self.play(Write(stage1_header))

        butterflies_s1 = VGroup()
        
        # Butterfly par superior (x0, x2)
        lines1, w1, n1 = create_butterfly(0, 0, 1, r"\zeta_2^0")
        # Butterfly par inferior (x1, x3)
        lines2, w2, n2 = create_butterfly(0, 2, 1, r"\zeta_2^0")
        
        self.play(
            Create(lines1), Write(w1), FadeIn(n1),
            Create(lines2), Write(w2), FadeIn(n2),
            run_time=1.5
        )
        
        # Pontos intermediários
        mid_nodes = VGroup()
        for y in row_y:
            mid_nodes.add(Dot([col_x[1], y, 0], color=YELLOW))
        
        self.play(Create(mid_nodes))
        self.wait(0.5)

        # --- 3. Estágio 2 (Combinar resultados para 4 pontos) ---
        # Borboletas span=2 (intercaladas)
        # Pesos: zeta_4^0 para o par superior, zeta_4^1 para o par inferior
        
        self.play(Write(stage2_header))
        
        # Precisamos desenhar 2 borboletas entrelaçadas
        # 1ª: Conecta Linha 0 e Linha 2 (Peso zeta^0)
        lines3, w3, n3 = create_butterfly(1, 0, 2, r"\zeta_4^0")
        
        # 2ª: Conecta Linha 1 e Linha 3 (Peso zeta^1)
        lines4, w4, n4 = create_butterfly(1, 1, 2, r"\zeta_4^1")
        
        self.play(
            Create(lines3), Write(w3), FadeIn(n3),
            Create(lines4), Write(w4), FadeIn(n4),
            run_time=2
        )
        
        # --- 4. Saídas Finais ---
        out_nodes = VGroup()
        out_labels = VGroup()
        
        # Ordem de saída é natural: 0, 1, 2, 3
        final_indices = [0, 1, 2, 3]
        
        for i, idx in enumerate(final_indices):
            dot = Dot(point=[col_x[2], row_y[i], 0], color=GREEN)
            label = MathTex(f"X[{idx}]").next_to(dot, RIGHT)
            out_nodes.add(dot)
            out_labels.add(label)
            
        header_out = Text("Saída (Frequência)", font_size=20, color=GREEN).next_to(out_nodes, UP, buff=0.5)

        self.play(
            Create(out_nodes),
            Write(out_labels),
            FadeIn(header_out)
        )
        
        # --- 5. Animação de Fluxo (Opcional, mas legal) ---
        # Faz bolinhas percorrerem o caminho para dar vida
        
        self.wait(1)
        
        path_example = VGroup()
        # Exemplo: Caminho de x[1] até X[2]
        # x[1] é índice 2 na lista row_y (-1.0) -> nó (0, 2)
        # Vai para nó intermediário (1, 3) (linha de baixo)
        # Vai para nó final (2, 2)
        
        p1 = np.array([col_x[0], row_y[2], 0]) # x[1]
        p2 = np.array([col_x[1], row_y[2], 0]) # Meio baixo
        p3 = np.array([col_x[2], row_y[0], 0]) # X[0]? Não, vamos fazer um caminho visual genérico
        
        # Vamos iluminar todas as linhas brevemente
        self.play(
            lines1.animate.set_color(YELLOW),
            lines2.animate.set_color(YELLOW),
            lines3.animate.set_color(GREEN),
            lines4.animate.set_color(GREEN),
            rate_func=there_and_back,
            run_time=2
        )

        # Notas Finais
        formula = MathTex(r"\zeta_N^k = e^{-i 2\pi k / N}").to_edge(DOWN)
        bbox = BackgroundRectangle(formula, color=BLACK, fill_opacity=0.8)
        self.play(Create(bbox), Write(formula))
        
        self.wait(2)