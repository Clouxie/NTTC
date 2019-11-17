import argparse
import scipy.io as sci
import numpy as np

class QPSK:

	nStreams = 2
	nMod = 2
	nFrames = 100
	mainRate = (0 , 1)

	def __init__(self , input_path  , output_path , nLdpc):
		
		matlabFiles = sio.loadmat(input_path)
		self.rate = mainRate
		self.nLdpc = nLdpc
		self.inputData = matlabFiles["v"][0][0]
		self.correctOutputData = matlabFiles["y"][0][0]
		self.outputData = np.zeros((int(self.nLdpc/self.nStreams), self.nStreams, self.nFrames), dtype = bool)
		
		
	def demultiplex(self):
		for frameIndex in range(self.nFrames):
			for bitIndex in range(self.nLdpc):
				nStream = self.rate[bitIndex%self.nStreams]
				mBitIndex = int(math.floor(bitIndex/self.nStreams))
				bit = self.inputData[bitIndex][frameIndex]
				self.outputData[mBitIndex][nStream][frameIndex] = bit
		self.outputData = np.reshape(self.outputData, (int(self.nLdpc/self.nMod), self.nMod, self.nFrames))
		checkResult(self)
		save(self)
		
	def checkResult(self):
		match = np.all(self.correctOutputData == self.outputData)
		print(f"Match: {match}")

	def save(self):
		mat = {"y": self.outputData}
		sio.savemat(f"out_{output_path}", mat)


class QAM16:

	nStreams = 8
	nMod = 4
	nFrames = 100	
	rate16200 = (7, 1, 4, 2, 5, 3, 6, 0)
	rate64000 = (0, 5, 1, 2, 4, 7, 3, 6)
    
	rates = {
		"16200": rate16200,
		"64800": rate64000,
	}

	def __init__(self, input_path , output_path , nLdpc):
		
		matlabFiles = sio.loadmat(input_path)
		self.rate = self.rates[nLdpc]
		self.nLdpc = nLdpc
		self.inputData = matlabFiles["v"][0][0]
		self.correctOutputData = matlabFiles["y"][0][0]
		self.outputData = np.zeros((int(self.nLdpc/self.nStreams), self.nStreams, self.nFrames), dtype = bool)
		
		
	def demultiplex(self):
		for frameIndex in range(self.nFrames):
			for bitIndex in range(self.nLdpc):
				nStream = self.rate[bitIndex%self.nStreams]
				mBitIndex = int(math.floor(bitIndex/self.nStreams))
				bit = self.inputData[bitIndex][frameIndex]
				self.outputData[mBitIndex][nStream][frameIndex] = bit
		self.outputData = np.reshape(self.outputData, (int(self.nLdpc/self.nMod), self.nMod, self.nFrames))
		
		
	def checkResult(self):
		match = np.all(self.correctOutputData == self.outputData)
		print(f"Match: {match}")
		return match


	def save(self):
		mat = {"y": self.outputData}
		sio.savemat(f"out_{output_path}", mat)



class qam256_64800:
	nStreams = 16
	nMod = 8
	nLdpc = 64800
	nFrames = 100
	
	rate35 = (2, 11, 3, 4, 0, 9, 1, 8, 10, 13, 7, 14, 6, 15, 5, 12)
	rate23 = (7, 2, 9, 0, 4, 6, 13, 3, 14, 10, 15, 5, 8, 12, 11, 1)
	rateRest = (15, 1, 13, 3, 8, 11, 9, 5, 10, 6, 4, 7, 12, 2, 14, 0)

	rates = {
		"2/3": rate23,
		"3/5": rate35,
		"rest": rateRest
	}

	def __init__(self, rate , input_path , save_path):
		
		matlabFiles = sio.loadmat(input_path)
		self.rate = self.rates[rate]
		self.save_path = save_path
		self.inputData = matlabFiles["v"][0][0]
		self.correctOutputData = matlabFiles["y"][0][0]
		self.outputData = np.zeros((int(self.nLdpc/self.nStreams), self.nStreams, self.nFrames), dtype = bool)
		
		
	def demultiplex(self):
		for frameIndex in range(self.nFrames):
			for bitIndex in range(self.nLdpc):
				nStream = self.rate[bitIndex%self.nStreams]
				mBitIndex = int(math.floor(bitIndex/self.nStreams))
				bit = self.inputData[bitIndex][frameIndex]
				self.outputData[mBitIndex][nStream][frameIndex] = bit
		self.outputData = np.reshape(self.outputData, (int(self.nLdpc/self.nMod), self.nMod, self.nFrames))
		
		
	def checkResult(self):
		match = np.all(self.correctOutputData == self.outputData)
		print(f"Match: {match}")
		return match


	def save(self):
		mat = {"y": self.outputData}
		sio.savemat(f"out_{self.save_path}", mat)



class Demultiplexer:
    
    def __init__(self, n_ldpc: int, n_cells: int, n_substreams: int, input_file: str ,  save_file : str) -> None:
        self.n_frames = 100
        self.n_ldpc = n_ldpc
        self.n_cells = n_cells
        self.save_path = save_file
        self.n_substreams = n_substreams
        self.input_file = input_file
        self.input_data_file = np.zeros((self.n_ldpc, self.n_frames))
        self.output_data_file = np.zeros(
            (self.n_cells, self.n_substreams, self.n_frames)
        )
        self.output_data = np.zeros(
            (self.n_cells, self.n_substreams, self.n_frames), dtype=bool
        )

    def get_data_from_file(self) -> None:
        try:
            data_from_file = sci.loadmat(self.input_file)
        except IOError:
            print("Error: can't find input file!")
        self.input_data_file = np.array(data_from_file["v"])[0][0]
        self.output_data_file = np.array(data_from_file["y"])[0][0]

    def transform_input_data(self) -> None:
        for frame_number in range(self.n_frames):
            for bit_number in range(int(self.n_ldpc / self.n_substreams)):
                temp_input_data = self.input_data_file[
                    bit_number * 8 : (bit_number + 1) * 8, frame_number
                ]

                self.output_data[bit_number, :, frame_number] = np.array(
                    [
                        temp_input_data[7],
                        temp_input_data[2],
                        temp_input_data[4],
                        temp_input_data[1],
                        temp_input_data[6],
                        temp_input_data[3],
                        temp_input_data[5],
                        temp_input_data[0],
                    ]
                )

    def save_data_as_npy(self) -> None:
        np.save(self.save_path, self.output_data)

    def save_data_as_mat(self) -> None:
        dict_out = {"y": self.output_data}
        sci.savemat(self.save_path, dict_out)
		
def main():
	print("Please run script with input arguments : --input_path --modulation --nLdpc --code_rate --output_path ")
	parser = argparse.ArgumentParser()
	parser.add_argument('--input_path', default='', help='Input path of Mat file')
	parser.add_argument('--modulation', default='', help='Chosing modulation QAM , QPSK etc')
	parser.add_argument('--nLdpc', default='16200', help='16200 or 64800')
	parser.add_argument('--code_rate', default='3/5', help='code rate for modulation , N/5 ...')
	parser.add_argument('--output_path', default='output.mat', help='Path to output modulated file')
	args = parser.parse_args()
    
	if args.modulation == 'QPSK':
        	QPSK = QPSK(args.input_path , args.output_path , args.nLdpc)
	elif args.modulation == '16QAM':
        	QAM16 = QAM16(args.input_path , args.output_path , args.nLdpc)  
	elif args.modulation == '64QAM':
        	#  # Get into
        	data_to_demux = Demultiplexer(
        	n_ldpc=16200,
        	n_cells=2025,
        	n_substreams=8,
        	input_file=args.input_path) 
	elif args.modulation == '256QAM':
        	qam23 = qam256_64800("rest")
        	qam23.demultiplex()
        	qam23.checkResult()
        	qam23.save()

    


if __name__ == '__main__':
	main()
