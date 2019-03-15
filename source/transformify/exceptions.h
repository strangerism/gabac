#ifndef TRANSFORMIFY_EXCEPTIONS_H_
#define TRANSFORMIFY_EXCEPTIONS_H_


#define TRANSFORMIFY_DIE(message) TRANSFORMIFY_THROW_RUNTIME_EXCEPTION(message)

#define TRANSFORMIFY_THROW_RUNTIME_EXCEPTION(message) \
    throw transformify::RuntimeException(__FILE__, __FUNCTION__, __LINE__, message)


#include <exception>
#include <iostream>
#include <string>


namespace transformify {


class Exception : public std::exception
{
 public:
    explicit Exception(
            const std::string& message
    );

    ~Exception() noexcept override;

    virtual std::string message() const;

    const char *what() const noexcept override;

 protected:
    std::string m_message;
};


class RuntimeException : public Exception
{
 public:
    explicit RuntimeException(
            const std::string& file,
            const std::string& function,
            int line,
            const std::string& message
    ) noexcept;

    RuntimeException(
            const RuntimeException& e
    ) noexcept;

    ~RuntimeException() noexcept override;
};


}  // namespace transformify


#endif  // TRANSFORMIFY_EXCEPTIONS_H_
