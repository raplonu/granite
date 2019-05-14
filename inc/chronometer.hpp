#ifndef GRANITE_CHRONOMETER_HPP
#define GRANITE_CHRONOMETER_HPP
#pragma once

namespace granite {
    namespace clock {

        /**
         * @brief A simple chronometer that measure time between creation and call of lifetime
         * 
         * @tparam Clock A Clock type that meet the Clock concept
         * See also : https://en.cppreference.com/w/cpp/named_req/Clock
         */
        template<typename Clock>
        struct chronometer {
            using clock = Clock;
            using rep =         typename clock::rep;
            using period =      typename clock::period;
            using duration =    typename clock::duration;
            using time_point =  typename clock::time_point;

            const time_point start_time;

            chronometer() : start_time(clock::now()) {}
            
            duration lifetime() noexcept(noexcept(clock::now())) const {
                return clock::now() - start_time;
            }
        };
    }
}

#endif //GRANITE_CHRONOMETER_HPP