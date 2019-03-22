#include "gabac/stream_handler.h"
#include "gabac/data_block.h"
#include "gabac/exceptions.h"


namespace gabac {

FileBuffer::FileBuffer(FILE *f) : fileptr(f){

}

int FileBuffer::overflow(int c){
    return fputc(c, fileptr);
}

std::streamsize FileBuffer::xsputn(const char *s, std::streamsize n){
    return fwrite(s, 1, n, fileptr);
}

int FileBuffer::sync(){
    return fflush(fileptr);
}

std::streamsize FileBuffer::xsgetn(char *s, std::streamsize n){
    return fread(s, 1, n, fileptr);
}

int FileBuffer::underflow(){
    return fgetc(fileptr);
}


size_t StreamHandler::readStream(std::istream& input, DataBlock *buffer){
    uint64_t streamSize = 0;
    input.read(reinterpret_cast<char *>(&streamSize), sizeof(uint64_t));
    return readBytes(input, streamSize, buffer);
}

size_t StreamHandler::readBytes(std::istream& input, size_t bytes, DataBlock *buffer){
    if (bytes % buffer->getWordSize()) {
        GABAC_THROW_RUNTIME_EXCEPTION("Input stream length not a multiple of word size");
    }
    buffer->resize(bytes / buffer->getWordSize());
    input.read(static_cast<char *>(buffer->getData()), bytes);
    return bytes;
}

size_t StreamHandler::readFull(std::istream& input, DataBlock *buffer){
    auto safe = input.exceptions();
    input.exceptions(std::ios::badbit);

    const size_t BUFFER_SIZE = 1000000 / buffer->getWordSize();
    buffer->resize(0);
    while (input.good()) {
        size_t pos = buffer->size();
        buffer->resize(pos + BUFFER_SIZE);
        input.read(
                static_cast<char *>(buffer->getData()) + pos * buffer->getWordSize(),
                BUFFER_SIZE * buffer->getWordSize());
    }
    if (!input.eof()) {
        GABAC_THROW_RUNTIME_EXCEPTION("Error while reading input stream");
    }
    if (input.gcount() % buffer->getWordSize()) {
        GABAC_THROW_RUNTIME_EXCEPTION("Input stream length not a multiple of word size");
    }
    buffer->resize(buffer->size() - (BUFFER_SIZE - input.gcount() / buffer->getWordSize()));
    input.exceptions(safe);
    return buffer->size();
}

size_t StreamHandler::readBlock(std::istream& input, size_t bytes, DataBlock *buffer){
    auto safe = input.exceptions();
    input.exceptions(std::ios::badbit);

    if (bytes % buffer->getWordSize()) {
        GABAC_THROW_RUNTIME_EXCEPTION("Input stream length not a multiple of word size");
    }
    const size_t BUFFER_SIZE = bytes / buffer->getWordSize();
    buffer->resize(BUFFER_SIZE);
    input.read(static_cast<char *>(buffer->getData()), BUFFER_SIZE * buffer->getWordSize());
    if (!input.good()) {
        if (!input.eof()) {
            GABAC_THROW_RUNTIME_EXCEPTION("Error while reading input stream");
        }
        buffer->resize(buffer->size() - (BUFFER_SIZE - input.gcount()));
    }
    input.exceptions(safe);
    return buffer->size();
}

size_t StreamHandler::writeStream(std::ostream& output, DataBlock *buffer){
    uint64_t size = buffer->getRawSize();
    output.write(reinterpret_cast<char *>(&size), sizeof(uint64_t));
    return writeBytes(output, buffer);
}

size_t StreamHandler::writeBytes(std::ostream& output, DataBlock *buffer){
    size_t ret = buffer->getRawSize();
    output.write(static_cast<char *>(buffer->getData()), ret);
    buffer->clear();
    return ret;
}


DataBlockBuffer::DataBlockBuffer(DataBlock *d, size_t pos_i) : block(0, 1), pos(pos_i){
    block.swap(d);
}

int DataBlockBuffer::overflow(int c){
    block.push_back(c);
    return c;
}

std::streamsize DataBlockBuffer::xsputn(const char *s, std::streamsize n){
    if (n % block.getWordSize()) {
        GABAC_THROW_RUNTIME_EXCEPTION("Invalid Data length");
    }
    size_t oldSize = block.size();
    block.resize(block.size() + n / block.getWordSize());
    memcpy(static_cast<uint8_t *>(block.getData()) + oldSize * block.getWordSize(), s, n);
    return n;
}

std::streamsize DataBlockBuffer::xsgetn(char *s, std::streamsize n){
    if (n % block.getWordSize()) {
        GABAC_THROW_RUNTIME_EXCEPTION("Invalid Data length");
    }
    size_t bytesRead = std::min(block.getRawSize() - pos * block.getWordSize(), size_t(n));
    memcpy(s, static_cast<uint8_t *>(block.getData()) + pos * block.getWordSize(), bytesRead);
    pos += bytesRead / block.getWordSize();
    return bytesRead;
}

int DataBlockBuffer::underflow(){
    if (pos == block.size()) {
        return EOF;
    }
    return block.get(pos);
}

int DataBlockBuffer::uflow(){
    if (pos == block.size()) {
        return EOF;
    }
    return block.get(pos++);
}

void DataBlockBuffer::flush_block(gabac::DataBlock *blk){
    block.swap(blk);
}


}