// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2023 The HepMC collaboration (see AUTHORS for details)
//
#ifndef HEPMC3_WRITEREDM4HEP_H
#define HEPMC3_WRITEREDM4HEP_H
///
/// @file  WriterEDM4HEP.h
/// @brief Definition of class \b WriterEDM4HEP
///
/// @class HepMC3::WriterEDM4HEP
/// @brief GenEvent I/O serialization for structured text files
///
/// @ingroup IO
///
#include "HepMC3/Writer.h"
#include "HepMC3/GenEvent.h"
#include "HepMC3/GenRunInfo.h"
#include <string>
#include <fstream>

namespace HepMC3
{

class WriterEDM4HEP : public Writer
{
public:

    /// @brief Constructor
    /// @warning If file already exists, it will be cleared before writing
    WriterEDM4HEP(const std::string& filename,
                      std::shared_ptr<GenRunInfo> run = std::shared_ptr<GenRunInfo>());

    /// @brief Constructor from ostream
    WriterEDM4HEP(std::ostream& stream,
                      std::shared_ptr<GenRunInfo> run = std::shared_ptr<GenRunInfo>());
    /// @brief Constructor from temp ostream
    WriterEDM4HEP(std::shared_ptr<std::ostream> s_stream,
                      std::shared_ptr<GenRunInfo> run = std::shared_ptr<GenRunInfo>());

    /// @brief Destructor
    ~WriterEDM4HEP();

    /// @brief Write event to file
    ///
    /// @param[in] evt Event to be serialized
    void write_event(const GenEvent& evt)  override;

    /// @brief Write the GenRunInfo object to file.
    void write_run_info();

    /// @brief Return status of the stream
    bool failed()  override;

    /// @brief Close file stream
    void close()  override;

    /// @brief Set output precision
    ///
    /// Available range is [2,24]. Default is 16.
    void set_precision( const int& prec );

    /// @brief Return output precision
    int precision() const;
private:

    /// @name Buffer management
    /// @{

    /// @brief Attempts to allocate buffer of the chosen size
    ///
    /// This function can be called manually by the user or will be called
    /// before first read/write operation
    ///
    /// @note If buffer size is too large it will be divided by 2 until it is
    /// small enough for system to allocate
    void allocate_buffer();

    /// @brief Set buffer size (in bytes)
    ///
    /// Default is 256kb. Minimum is 256b.
    /// Size can only be changed before first read/write operation.
    void set_buffer_size(const size_t& size );

    /// @brief Escape '\' and '\n' characters in string
    std::string escape(const std::string& s)  const;

    /// Inline function flushing buffer to output stream when close to buffer capacity
    void flush();

    /// Inline function forcing flush to the output stream
    void forced_flush();

    /// @}


    /// @name Write helpers
    /// @{

    /// @brief Inline function for writing strings
    ///
    /// Since strings can be long (maybe even longer than buffer) they have to be dealt
    /// with separately.
    void write_string(const std::string &str );

    /// @brief Write vertex
    ///
    /// Helper routine for writing single vertex to file
    void write_vertex(const ConstGenVertexPtr& v);

    /// @brief Write particle
    ///
    /// Helper routine for writing single particle to file
    void write_particle(const ConstGenParticlePtr& p, int second_field);

    /// @}

private:

    std::ofstream m_file; //!< Output file
    std::shared_ptr<std::ostream> m_shared_stream;///< Output temp. stream
    std::ostream* m_stream; //!< Output stream
    int m_precision; //!< Output precision
    char* m_buffer;  //!< Stream buffer
    char* m_cursor;  //!< Cursor inside stream buffer
    unsigned long m_buffer_size; //!< Buffer size
    unsigned long m_particle_counter; //!< Used to set bar codes
    std::string m_float_printf_specifier; //!< the specifier of printf used for floats
};


} // namespace HepMC3

#endif
