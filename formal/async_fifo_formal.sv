module async_fifo_formal;
  localparam int DATA_WIDTH = 8;
  localparam int ADDR_WIDTH = 2;

  logic wr_clk;
  logic rd_clk;
  logic wr_rst_n;
  logic rd_rst_n;
  logic wr_en;
  logic rd_en;
  logic [DATA_WIDTH-1:0] wr_data;
  logic [DATA_WIDTH-1:0] rd_data;
  logic full;
  logic empty;

  async_fifo #(.DATA_WIDTH(DATA_WIDTH), .ADDR_WIDTH(ADDR_WIDTH)) dut (.*);

  always #1 wr_clk = ~wr_clk;
  always #2 rd_clk = ~rd_clk;

  always_ff @(posedge wr_clk) begin
    if (wr_rst_n && full && wr_en) begin
      assert($stable(dut.wr_bin));
    end
  end

  always_ff @(posedge rd_clk) begin
    if (rd_rst_n && empty && rd_en) begin
      assert($stable(dut.rd_bin));
    end
  end
endmodule
